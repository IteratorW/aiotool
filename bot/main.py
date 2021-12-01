import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import Executor
from tortoise import Tortoise

from api.extension import extension_handler
from bot import env

bot = Bot(env.TELEGRAM_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
executor = Executor(dp, skip_updates=True)

logger = logging.getLogger("main")


# noinspection PyProtectedMember
async def run_aiogram():
    executor._prepare_polling()

    await executor._startup_polling()
    asyncio.create_task(executor.dispatcher.start_polling())


async def run_tortoise():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': extension_handler.extensions_models + ["api.models"]}
    )
    await Tortoise.generate_schemas()


async def run():
    logger.info("Running aiogram")

    await run_aiogram()

    logger.info("Running tortoise")

    await run_tortoise()
