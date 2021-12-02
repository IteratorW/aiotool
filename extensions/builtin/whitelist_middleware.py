from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from api.models import AiotoolUser


class WhitelistMiddleware(BaseMiddleware):
    async def on_process_message(self, message: Message, data: dict):
        whitelist_exempt = False

        handler = current_handler.get()

        if handler is not None:
            whitelist_exempt = getattr(handler, "whitelist_exempted", False)

        if not whitelist_exempt:
            aiotool_user = (await AiotoolUser.get_or_create(user_id=message.from_user.id))[0]

            if not aiotool_user.whitelisted:
                await message.reply("Извини, но тебя нет в вайтлисте.")

                raise CancelHandler

    async def on_process_callback_query(self, query: CallbackQuery, data: dict):
        whitelist_exempt = False

        handler = current_handler.get()

        if handler is not None:
            whitelist_exempt = getattr(handler, "whitelist_exempted", False)

        if not whitelist_exempt:
            aiotool_user = (await AiotoolUser.get_or_create(user_id=query.from_user.id))[0]

            if not aiotool_user.whitelisted:
                raise CancelHandler
