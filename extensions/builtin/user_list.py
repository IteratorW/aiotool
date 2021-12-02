from aiogram.types import Message, ParseMode
from aiogram.utils.markdown import hpre
from tabulate import tabulate

from api.menu.decorators import aiotool_menu_node_handler
from api.menu.menu_node import MenuNode
from api.models import AiotoolUser
from bot import main
from extensions.builtin.menu import admin_node


async def get_name_from_id(user_id: int):
    return (await main.bot.get_chat_member(user_id, user_id)).user.full_name


def b_name(value):
    return "Да" if value else "Нет"


@aiotool_menu_node_handler(MenuNode("user_list", "📘 Список пользователей", admin_only=True), admin_node)
async def user_list_handler(message: Message):
    table = [[await get_name_from_id(user.user_id), b_name(user.whitelisted), b_name(user.admin)] async for user in
             AiotoolUser.all()]
    result = tabulate(table, headers=["Пользователь", "В вайтлисте", "Админ"], tablefmt="pretty")

    await message.reply(hpre(result), parse_mode=ParseMode.HTML)
