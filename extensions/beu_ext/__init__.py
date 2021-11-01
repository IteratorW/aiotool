from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message

from api import const, main
from api.function.decorators import aiotool_function
from api.menu.decorators import aiotool_menu_entry
from api.state.custom_state import CustomState


class TestState(CustomState):
    @staticmethod
    async def on_state(message: Message, state: FSMContext):
        async with state.proxy() as data:
            data['test1'] = message.text

        await state.finish()


class TestForm(StatesGroup):
    test1 = TestState()


@aiotool_function(TestForm)
async def test_func(message: Message, state: FSMContext):
    async with state.proxy() as data:
        print(data)
        await message.reply(data["test1"])


@aiotool_menu_entry("❤ State test")
async def beubass_entry(message: types.Message):
    await TestForm.test1.set()

    await message.reply("Enter test value")
