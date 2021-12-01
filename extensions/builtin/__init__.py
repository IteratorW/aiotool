from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot import main
from api.menu import menu_handler
from extensions.builtin.whitelist_middleware import WhitelistMiddleware

from . import settings_form

main.dp.middleware.setup(WhitelistMiddleware())


@main.dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Добро пожаловать!", reply_markup=await menu_handler.get_node_keyboard(menu_handler.root_node))
