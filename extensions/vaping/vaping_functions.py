from datetime import datetime

from aiogram.types import Message, ParseMode
from aiogram.utils.markdown import hbold

from api.menu.decorators import aiotool_menu_node_handler
from api.menu.menu_node import MenuNode
from bot import main
from extensions.vaping import menu, plot
from extensions.vaping.models import VapingSettings
from extensions.vaping.month_names import MONTH_NAMES
from extensions.vaping.monthly_puff_data import MonthlyPuffData


top_numbers = {
    1: "1️⃣",
    2: "2️⃣",
    3: "3️⃣",
    4: "4️⃣",
    5: "5️⃣"
}


@aiotool_menu_node_handler(MenuNode("vaping_self_stats", "📊 Затяжки за текущий месяц"), menu.vaping_menu)
async def self_stats_handler(message: Message):
    puff_data = await MonthlyPuffData.get_for_user(message.from_user.id)

    if puff_data is None:
        await message.reply("За этот месяц у тебя не записано или записано слишком мало затяжек! Попробуй завтра.")

        return

    await main.bot.send_photo(message.chat.id, photo=plot.get_vaping_plot_month([puff_data]),
                              caption=f"""
Статистика твоих затяжек за {MONTH_NAMES[datetime.now().month - 1].lower()}:
Всего затяжек: {hbold(puff_data.all_puffs)}
В среднем за день: {hbold(puff_data.mean)}
                              """, parse_mode=ParseMode.HTML)


@aiotool_menu_node_handler(MenuNode("vaping_global_stats", "🏆 Статистика затяжек (Глобальная)"), menu.vaping_menu)
async def global_stats_handler(message: Message):
    puff_data_list = []

    async for vaping_entry in VapingSettings.all():
        if vaping_entry.vaping_activated:
            puff_data = await MonthlyPuffData.get_for_user(vaping_entry.user_id)

            if puff_data is not None:
                puff_data_list.append(puff_data)

    if not len(puff_data_list):
        await message.reply("Пока что никто не участвует в топе. Попробуй завтра.")

        return

    puff_data_list.sort(key=lambda x: x.all_puffs, reverse=True)
    puff_data_list = puff_data_list[:5]

    caption = ""

    for i, puff_data in enumerate(puff_data_list):
        caption += f"\n{top_numbers[i + 1]}. {puff_data.username} - {puff_data.all_puffs} затяжек"

    await main.bot.send_photo(message.chat.id, photo=plot.get_vaping_plot_month(puff_data_list, global_chart=True),
                              caption=caption)
