from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message

from extensions.builtin.models import AiotoolUser


class WhitelistMiddleware(BaseMiddleware):
    async def on_process_message(self, message: Message, data: dict):
        aiotool_user = (await AiotoolUser.get_or_create(user_id=message.from_user.id))[0]

        if not aiotool_user.whitelisted:
            await message.reply("Извини, но тебя нет в вайтлисте!")

            raise CancelHandler
