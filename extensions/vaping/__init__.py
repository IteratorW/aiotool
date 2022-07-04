import asyncio

import aioschedule

from api.postload import postload
from . import vaping_functions, reminding
from . import vaping_handler
from . import debug
from . import vaping_month_stats
from . import vaping_year_stats


async def schedule_task():
    while True:
        await aioschedule.run_pending()

        await asyncio.sleep(0.1)


@postload()
async def postload():
    await reminding.create_jobs()

    asyncio.create_task(schedule_task())
