from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from bot import const

bot = Bot(const.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


def run():
    executor.start_polling(dp, skip_updates=True)
