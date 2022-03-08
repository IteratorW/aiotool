import asyncio
import datetime
import logging

from aiohttp import ClientSession, ClientTimeout, ClientConnectionError

from api.postload import postload
from bot import main
from extensions.apex import env

VALID_MAP_CODE = "kings_canyon_rotation"

logger = logging.getLogger("apex map task")

next_check_time = None


async def request_map_data():
    session = ClientSession(timeout=ClientTimeout(5))

    params = {"version": "2",
              "auth": env.apex_api_key}

    try:
        response = await session.get("https://api.mozambiquehe.re/maprotation",
                                     params=params)
    except (asyncio.TimeoutError, ClientConnectionError):
        return None

    data = (await response.json(content_type="text/plain;charset=utf-8"))["battle_royale"]

    await session.close()
    response.close()

    return data


async def send_message(text: str):
    await main.bot.send_message(1295112341, text)


async def map_task():
    global next_check_time

    while True:
        current_time = datetime.datetime.now(datetime.timezone.utc).timestamp()

        if next_check_time is None or next_check_time < current_time:
            data = await request_map_data()

            if data is not None:
                next_check_time = data["current"]["end"]

                if data["current"]["code"] == VALID_MAP_CODE:
                    await send_message(
                        f"Warning: {data['current']['map']} is currently in rotation "
                        f"for {data['current']['remainingMins']} minutes.")

        await asyncio.sleep(60)


@postload()
async def postload():
    if env.apex_api_key:
        logger.info("Starting task.")

        asyncio.create_task(map_task())
    else:
        logger.error("Apex API key not specified.")
