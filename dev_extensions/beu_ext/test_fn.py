from aiogram.types import Message

from api.menu import menu_handler
from api.menu.decorators import aiotool_menu_node_handler
from api.menu.menu_node import MenuNode
from api.state.auto.auto_states import AutoStringState
from api.state.wrapped_states_group import WrappedStatesGroup
from dev_extensions.beu_ext.models import TestSettings

test_node = MenuNode("test_node", "❤️Тестовая категория")
menu_handler.add_node(test_node)


@aiotool_menu_node_handler(MenuNode("values_test", "Тест значений"), test_node)
async def test_handler(message: Message):
    inst = (await TestSettings.get_or_create(user_id=message.from_user.id))[0]

    await message.reply(f"""
test_string: {inst.test_string}
test_boolean: {inst.test_bool}
test_int: {inst.test_int}
    """)
