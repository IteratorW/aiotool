import statistics
from calendar import monthrange
from datetime import datetime

import pytz
from tortoise.query_utils import Q

from bot import main, env
from extensions.vaping.models import PuffEntry


class MonthlyPuffData:
    def __init__(self, puffs: list[int], month_days: int, username: str):
        self.puffs = puffs
        self.month_days = month_days
        self.username = username

    @property
    def all_puffs(self):
        return sum(self.puffs)

    @property
    def mean(self):
        return int(statistics.mean(self.puffs))

    @classmethod
    async def get_for_user(cls, user_id: int, month: int = -1):
        now = datetime.now()
        cur_month = now.month if month == -1 else month
        days_count = monthrange(now.year, cur_month)[1]

        puffs = []

        for day in range(1, days_count + 1):
            if not env.DEBUG and month == -1 and day > now.day - 1:
                break

            dt = pytz.utc.localize(datetime(year=now.year, month=cur_month, day=day))

            entries = await PuffEntry.filter(user_id=user_id, date=dt)

            puffs.append(0 if not len(entries) else entries[0].puffs)

        if len([puff_count for puff_count in puffs if puff_count != 0]) < 2:
            return None

        username = (await main.bot.get_chat_member(user_id, user_id)).user.full_name

        return cls(puffs, days_count, username)
