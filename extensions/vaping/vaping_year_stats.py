import datetime
import statistics

from aiogram.types import Message, ParseMode

from api.menu.decorators import aiotool_menu_node_handler
from api.menu.menu_node import MenuNode
from bot import main
from extensions.vaping import menu, plot
from extensions.vaping.monthly_puff_data import MonthlyPuffData


@aiotool_menu_node_handler(MenuNode("vaping_year_stats", "🗓️ Годовая статистика"), menu.vaping_menu)
async def self_year__stats_handler(message: Message):
    months_data = [await MonthlyPuffData.get_for_user(message.from_user.id, m) for m in
                   range(1, datetime.date.today().month + 1)]
    months_data = [puffs.all_puffs if puffs is not None else 0 for puffs in months_data]

    if max(months_data) == 0:
        await message.reply("За этот год у тебя не записано ни одной затяжки... Ой-ой-ой....")

        return

    await main.bot.send_photo(message.chat.id, photo=plot.get_vaping_plot_year(months_data),
                              caption=f"""
    Статистика твоих затяжек за {datetime.date.today().year} год:
    Всего затяжек: {sum(months_data)}
    В среднем за месяц: {int(statistics.mean(months_data))}
                                  """, parse_mode=ParseMode.HTML)
