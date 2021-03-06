import uuid

from aiogram.types import InlineKeyboardButton, Message, ParseMode, User
from aiogram.utils.deep_linking import get_start_link
from aiogram.utils.markdown import hbold, hlink

from api.menu.menu_node import MenuNode
from api.state.state_with_buttons import StateWithButtons
from api.state.wrapped_states_group import WrappedStatesGroup
from extensions.builtin.menu import admin_node
from extensions.builtin.models import InviteEntry


class InviteForm(WrappedStatesGroup):
    flag = StateWithButtons("Укажи флаги для этого инвайта",
                            InlineKeyboardButton(text="📝 Добавить в вайтлист"),
                            InlineKeyboardButton(text="📝✏️ Добавить в вайтлист и сделать админом"), use_int_ids=True,
                            optional=True)


@InviteForm.function(MenuNode("whitelist_invite", "➡️ Создать инвайт", admin_only=True), admin_node)
async def invite_function(message: Message, user: User, flag: int):
    if flag is None:
        flag = -1

    if flag != -1:
        invite_id = str(uuid.uuid4())[:32]
        invite_url = await get_start_link(invite_id)

        await InviteEntry.create(code=invite_id, flag=flag)
    else:
        invite_url = await get_start_link("")

    messages = {
        -1: "простой инвайт",
        0: "инвайт, который добавит пользователя в вайтлист",
        1: "инвайт, который добавит пользователя в вайтлист и сделает его админом"
    }

    await message.answer(f"""
Ты успешно сделал {hbold(messages[flag])}.

{hlink(url=invite_url, title=invite_url)}

Этот инвайт можно использовать только один рза.
""", parse_mode=ParseMode.HTML)
