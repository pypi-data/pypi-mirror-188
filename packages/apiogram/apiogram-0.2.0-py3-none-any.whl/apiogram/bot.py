import os
import aiogram
import asyncio
import logging
import pymongo
from aiogram import Dispatcher
from datetime import datetime
from aiogram.types import ParseMode
from aiogram.utils import exceptions
from aiogram.dispatcher.storage import BaseStorage
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from magic_config import Config
from nosql_storage_wrapper.mongo import Storage
from geekjob_python_helpers.fs import recursive_import
from .direction import BotDirection
from .helpers.middleware.msglogger import MessageLoggerMiddleware
from contextlib import suppress
from aiogram.utils.exceptions import (MessageCantBeDeleted,
                                      MessageToDeleteNotFound)

log = logging.getLogger("apiogram_log_messages")


def create_state_storage(storage_type: str | None = None) -> BaseStorage:
    """
    Create storage
    """
    match storage_type:
        case "mongo":
            return MongoStorage(host=Config.mongo_host,
                                port=Config.mongo_port,
                                username=Config.mongo_user,
                                password=Config.mongo_pwd,
                                db_name=Config.mongo_db)
        case "redis":
            raise NotImplementedError("Redis storage is not implemented yet")
        case "dragonfly":
            raise NotImplementedError("Dragonfly storage is not implemented yet")
        case _:
            return MemoryStorage()


async def log_sending_message_id(message: aiogram.types.Message, direction: int) -> None:
    """
    Log sending messages id
    """
    await Storage("chat_msg_id").insert_one({
        "chat_id": message.chat.id,
        "msg_id": message.message_id,
        "dir": direction,
        "datetime": datetime.now(),
    })


async def log_outgoing_message(chat_id: int, **kwargs) -> None:
    """
    Log outgoing messages
    """
    return await Storage("chat_log").insert_one({
        "chat_id": chat_id,
        "datetime": datetime.now(),
        "dir": BotDirection.Outgoing,
        "client": "aiogram",
        "data": {
            **kwargs
        }
    })


async def log_outgoing_message_error(chat_id: int, error: str) -> None:
    """
    Log outgoing messages error
    """
    await Storage("chat_error").insert_one({
        "chat_id": chat_id,
        "error": error
    })
    log.error(f"ID[{chat_id}]: {error}")


async def log_api_answer(chat_id: int, data: dict | object) -> None:
    """
    Log api answer
    @param chat_id:
    @param data:
    @return:
    """
    await Storage("api_log").insert_one({
        "chat_id": chat_id,
        "data": data
    })
    log.info(f"ID[{chat_id}]: {data}")


class BotEngine:
    """
    Singleton
    Create one instance of Telegram Bot

    Usage:
        from bot import Bot

        bot = Bot(telegram_token)

        @Bot.message_handler(...)
        async def handler(messages, state):
            ...

        executor.start_polling(bot)
    """

    __instance: "BotEngine" = None
    dispatch: Dispatcher = None
    bot = None

    def __new__(cls, *args, **kwargs) -> "BotEngine":
        """
        Create singleton instance of Telegram Bot
        """
        if not cls.__instance:
            cls.__instance = super(BotEngine, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self, token: str = None, storage_type: str = "memory", parse_mode: str = ParseMode.HTML):
        """
        Constructor
        Initialize bot instance
        """
        if token is None:
            return

        self.bot = aiogram.Bot(token=token, parse_mode=parse_mode)
        self.dispatch = aiogram.Dispatcher(self.bot, storage=create_state_storage(storage_type))
        __send_message = self.bot.send_message
        self.recursion_counter = 0

        async def wraped_send_message(**kwargs) -> aiogram.types.Message | None:
            err_str: str = ""
            success = False
            chat_id: int = kwargs["chat_id"]

            if "reply_markup" in kwargs and kwargs["reply_markup"] is not None:
                kwargs["reply_markup"] = str(kwargs["reply_markup"])

            await log_outgoing_message(**kwargs)
            res = None

            try:
                if Config.DEBUG_STEP:
                    cur_state = await self.get_current_state()
                    if "text" in kwargs and kwargs["text"] is not None:
                        kwargs["text"] = (f"\n┃ ⚠️ State: <b>{cur_state}</b>"
                                          "\n┗━━━━━━━━━━━━━━━━━━━━━━━━━"
                                          f"\n\n{kwargs['text']}")
                    # await __send_message(chat_id=chat_id, text=f"⚠️ State: {cur_state}")

                res = await __send_message(**kwargs)
                await log_sending_message_id(res, BotDirection.Outgoing)

            except exceptions.BotBlocked as e:
                err_str = "BotBlocked" + str(e)
            except exceptions.ChatNotFound as e:
                err_str = "ChatNotFound" + str(e)
            except exceptions.UserDeactivated as e:
                err_str = "UserDeactivated" + str(e)
            except exceptions.TelegramAPIError as e:
                err_str = "TelegramAPIError: " + str(e)
            except exceptions.RetryAfter as e:
                log.error(f"ID[{chat_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
                await log_outgoing_message_error(chat_id, err_str)
                await asyncio.sleep(e.timeout)
                if self.recursion_counter < 3:
                    self.recursion_counter += 1
                    return await wraped_send_message(**kwargs)  # Recursive call
                self.recursion_counter = 0
                err_str = "RetryAfter"
            else:
                success = True

            if not success:
                await log_outgoing_message_error(chat_id, err_str)
            return res

        self.bot.send_message = wraped_send_message

    def __call__(self, *args, **kwargs) -> aiogram.Dispatcher:
        """
        Call bot as function constructor like
        Example:
            bot = Bot(telegram_token)
        """
        self.__init__(*args, **kwargs)
        return self.dispatch

    def callback_query_handler(self, *args, **kwargs) -> callable:
        return self.dispatch.callback_query_handler(*args, **kwargs)

    def message_handler(self, *args, **kwargs) -> callable:
        return self.dispatch.message_handler(*args, **kwargs)

    async def answer(self, message: aiogram.types.Message, text: str, **kwargs) -> bool:
        """Send text messages to user"""
        if "reply_markup" in kwargs:
            kwargs["reply_markup"] = str(kwargs["reply_markup"])
        return await self.bot.answer(message, text=text, **kwargs)

    async def clear_previous_messages(self, chat_id: int, count: int = 1, direction: int = None) -> None:
        """Clear previous messages"""

        if Config.DEBUG and Config.DEBUG_PRESERVE_MSG:
            # preserve messages in debug mode
            return

        filter = {"chat_id": chat_id}
        if direction is not None:
            filter["dir"] = direction
        ids = [
            msg["msg_id"] async for msg in
            Storage("chat_msg_id").find(filter).sort("_id", pymongo.DESCENDING).limit(count)
        ]
        with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
            for id in ids:
                await self.bot.delete_message(chat_id, message_id=id)
        Storage("chat_msg_id").delete_many({"msg_id": {"$in": ids}})

    async def clear_previous_message(self, chat_id: int) -> None:
        """Clear previous messages"""
        return await self.clear_previous_messages(chat_id, count=1)

    async def delete_user_messages(self, chat_id: int, count: int = 1) -> None:
        """Delete user messages"""
        return await self.clear_previous_messages(chat_id, count=count, direction=BotDirection.Incoming)

    async def delete_bot_message(self, chat_id: int, count: int = 1) -> None:
        """Delete bot messages"""
        return await self.clear_previous_messages(chat_id, count=count, direction=BotDirection.Outgoing)

    async def download_file(self, message: aiogram.types.Message, file_id: str, file_unique_id: str) -> None:
        """Download file from telegram server"""
        dir_name = str(message.chat.id)
        os.makedirs("storage/cv/{}".format(dir_name), exist_ok=True)
        file_info = await self.bot.get_file(file_id)
        downloaded_file = await self.bot.download_file(file_info.file_path)
        file_name = message.document.file_name \
            if message.content_type == "document" \
            else file_info.file_path.replace("photos/", "")
        src = f"storage/cv/{dir_name}/" + file_unique_id + file_name[-4:]
        with open(src, "wb") as new_file:
            new_file.write(downloaded_file.getvalue())

    async def get_current_state(self) -> str:
        """Get current state"""
        return await self.dispatch.current_state().get_state()


def start_polling(telegram_token: str = Config.telegram_token) -> None:
    """
    Start Telegram Bot API server
    """
    # Only for debug, delete my state
    if Config.DEBUG and Config.DEBUG_USER_ID:
        log.info(f"⚙️   Reset data for debug user: {Config.DEBUG_USER_ID}")

        log.info("Clear chat_log...")
        Storage("chat_log").delete_one({"chat": Config.DEBUG_USER_ID})

        log.info("Clear aiogram_state...")
        Storage("aiogram_state").delete_one({"chat": Config.DEBUG_USER_ID})

    log.debug("⏯ Run main functionality")
    # Get Bot instance and configurate it
    bot = Bot(telegram_token, storage_type="mongo")

    # Register defualt core handler for logging all messages
    bot.middleware.setup(MessageLoggerMiddleware())

    if os.path.exists("helpers/middleware"):
        import apiogram.helpers.middleware as middlewares
        logging.debug(f"⚙️   Setup middleware from {middlewares.__name__}")
        for key in dir(middlewares):
            if key.startswith("_"):
                continue
            middleware = getattr(middlewares, key)
            # if callable(middleware) and isinstance(middleware, aiogram.dispatcher.middlewares.BaseMiddleware):
            if isinstance(middleware, aiogram.dispatcher.middlewares.BaseMiddleware):
                instance = middleware()
                bot.middleware.setup(instance)

    # Import all modules from modules folder
    recursive_import("dialog_handlers")

    # Start bot
    aiogram.utils.executor.start_polling(bot, skip_updates=False)


# Singleton instance
Bot = BotEngine()
