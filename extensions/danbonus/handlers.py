from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from api.menu.decorators import aiotool_menu_node_handler
from api.menu.menu_node import MenuNode
from extensions.danbonus import markup


@aiotool_menu_node_handler(MenuNode("secret_code", "Указать секретный код"))
async def on_secret_code(message: Message):
    await message.reply("Укажи секретный код.")

    await message.answer("-", reply_markup=markup.get_markup())
