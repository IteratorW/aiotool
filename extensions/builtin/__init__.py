from aiogram import types

from api import main
from api.menu import menu_handler


@main.dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Добро пожаловать!", reply_markup=menu_handler.get_keyboard())
