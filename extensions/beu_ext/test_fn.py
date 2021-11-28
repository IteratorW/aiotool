from aiogram.types import InlineKeyboardButton, Message
from tortoise.exceptions import ValidationError

from api.menu.decorators import aiotool_menu_entry
from api.state.auto.auto_states import AutoStringState
from api.state.state_with_buttons import StateWithButtons
from api.state.wrapped_states_group import WrappedStatesGroup
from extensions.beu_ext.models import TestSettings


class TestForm(WrappedStatesGroup):
    state_1 = AutoStringState("Введи что угодно")


@TestForm.function(menu="Test")
async def test_fn(message: Message, state_1: str):
    pass


@aiotool_menu_entry("Тест значений")
async def test_handler(message: Message):
    inst = (await TestSettings.get_or_create(user_id=message.from_user.id))[0]

    await message.reply(f"""
test_string: {inst.test_string}
test_boolean: {inst.test_bool}
test_int: {inst.test_int}
    """)
