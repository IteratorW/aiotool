from datetime import date

from aiogram.types import Message, InlineKeyboardButton, User, InlineKeyboardMarkup, CallbackQuery, ParseMode
from aiogram.utils.markdown import hbold

import bot.main
from api.menu.decorators import aiotool_menu_node_handler
from api.menu.menu_node import MenuNode
from api.state.state_with_buttons import StateWithButtons
from api.state.wrapped_states_group import WrappedStatesGroup
from bot import main
from extensions.vaping import menu, plot
from extensions.vaping.month_names import MONTH_NAMES
from extensions.vaping.monthly_puff_data import MonthlyPuffData


@aiotool_menu_node_handler(MenuNode("vaping_month_stats", "📅 Затяжки за прошлые месяцы"), menu.vaping_menu)
async def self_month_stats_handler(message: Message):
    kb = InlineKeyboardMarkup()

    for i in range(0, date.today().month):
        kb.add(InlineKeyboardButton(text=MONTH_NAMES[i], callback_data=f"vaping_month_{i}"))

    await message.reply("Выбери месяц:", reply_markup=kb)


@main.dp.callback_query_handler(lambda query: query.data.startswith("vaping_month_"))
async def vaping_month_handler(query: CallbackQuery):
    await query.answer()

    try:
        month_num = int(query.data.split("_")[2])
    except ValueError:
        return

    puff_data = await MonthlyPuffData.get_for_user(query.from_user.id, month_num + 1)

    if not puff_data:
        await query.message.answer("За этот месяц информация отсутствует.")

        return

    await main.bot.send_photo(query.message.chat.id, photo=plot.get_vaping_plot_month([puff_data]),
                              caption=f"""
    Статистика твоих затяжек за {MONTH_NAMES[month_num].lower()}:
    Всего затяжек: {hbold(puff_data.all_puffs)}
    В среднем за день: {hbold(puff_data.mean)}
                                  """, parse_mode=ParseMode.HTML)
