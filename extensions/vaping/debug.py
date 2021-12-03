import random
from calendar import monthrange
from datetime import datetime

import pytz
from aiogram.types import Message

from api.menu.decorators import aiotool_menu_node_handler
from api.menu.menu_node import MenuNode
from bot import env
from extensions.vaping.menu import vaping_menu
from extensions.vaping.models import PuffEntry

if env.DEBUG:
    @aiotool_menu_node_handler(MenuNode("vaping_debug", "Сгенерировать рандомные "
                                                        "затяжки за текущий месяц"), vaping_menu)
    async def vaping_debug_handler(message: Message):
        now = datetime.now()
        days_count = monthrange(now.year, now.month)[1]

        for day in range(1, days_count + 1):
            dt = pytz.utc.localize(datetime(year=now.year, month=now.month, day=day))

            entries = await PuffEntry.filter(user_id=message.from_user.id, date=dt)

            if not len(entries):
                await PuffEntry.create(user_id=message.from_user.id, puffs=random.randrange(10, 560), date=dt)

        await message.reply("Успешно!")
