from typing import Optional

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, User, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.markdown import hbold

from api.menu.menu_node import MenuNode
from api.models import AiotoolUser
from api.state.state_result import StateResult
from api.state.wrapped_state import WrappedState
from api.state.wrapped_states_group import WrappedStatesGroup
from bot import main
from extensions.builtin.menu import admin_node


class UserIDState(WrappedState):
    async def on_state(self, message: Message, state: FSMContext) -> Optional[StateResult]:
        username = message.text[1:] if message.text.startswith("@") else message.text

        user = None
        async for user in AiotoolUser.all():
            member = await main.bot.get_chat_member(user.user_id, user.user_id)

            if member.user.username == username:
                user = member.user
                break

        if user is None:
            await message.reply("Пользователь не найден!"
                                "\nВы можете указать только того пользователя, который хотя бы один раз писал боту.")
            return None

        await state.update_data({"user": user})

        return StateResult.COMPLETED


class EditUserForm(WrappedStatesGroup):
    username = UserIDState("Укажи username пользователя")


def get_user_text(user: User, aiotool_user: AiotoolUser):
    return f"""
Пользователь {hbold(user.full_name)} ({user.username})

В вайтлисте: {hbold("Да" if aiotool_user.whitelisted else "Нет")}
Админ: {hbold("Да" if aiotool_user.admin else "Нет")}
"""


def get_markup(aiotool_user: AiotoolUser):
    kb = InlineKeyboardMarkup()

    whitelisted = aiotool_user.whitelisted
    is_admin = aiotool_user.admin

    kb.insert(InlineKeyboardButton(text="🟥 Убрать из вайтлиста" if whitelisted else "🟩 Добавить в вайтлист",
                                   callback_data=f"edit_user_{aiotool_user.user_id}_whitelisted_{not whitelisted}"))
    kb.insert(InlineKeyboardButton(text="🟥 Убрать права админа" if is_admin else "🟩 Сделать админом",
                                   callback_data=f"edit_user_{aiotool_user.user_id}_admin_{not is_admin}"))

    return kb


@main.dp.callback_query_handler(lambda query: query.data.startswith("edit_user_"))
async def edit_callback(query: CallbackQuery):
    data = query.data.split("_")

    if len(data) < 5:
        return

    user_id = data[2]
    field = data[3]
    value = data[4] == "True"

    if field not in ("admin", "whitelisted"):
        return

    aiotool_user = await AiotoolUser.get(user_id=user_id)
    await aiotool_user.update_from_dict({field: value})
    await aiotool_user.save()

    user = (await main.bot.get_chat_member(user_id, user_id)).user

    await query.message.edit_text(get_user_text(user, aiotool_user), reply_markup=get_markup(aiotool_user),
                                  parse_mode=ParseMode.HTML)


@EditUserForm.function(MenuNode("edit_user", "✔️ Редактировать пользователя"), admin_node)
async def edit_user_function(message: Message, user: User):
    aiotool_user = await AiotoolUser.get(user_id=user.id)

    await message.answer(get_user_text(user, aiotool_user), parse_mode=ParseMode.HTML,
                         reply_markup=get_markup(aiotool_user))
