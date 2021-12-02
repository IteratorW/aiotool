from aiogram.types import Message

from api.menu import menu_handler
from api.models import AiotoolUser
from api.whitelist_exempt import whitelist_exempt
from bot import main
from .models import InviteEntry


@whitelist_exempt()
@main.dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: Message):
    payload = message.get_args()

    user = (await AiotoolUser.get_or_create(user_id=message.from_user.id))[0]

    if len(payload) > 0:
        invite = await InviteEntry.get_or_none(code=payload)

        if invite is not None:
            if invite.used:
                await message.answer("Этот инвайт уже был использован!")

                return

            await message.answer(
                f"Ты успешно вошёл по "
                f"инвайту и теперь {'добавлен в вайтлист' if invite.flag == 0 else 'стал админом'}!")

            invite.used = True
            await invite.save()

            user.whitelisted = True
            user.admin = invite.flag == 1
            await user.save()
        else:
            await message.answer("Неверный инвайт!")

            return
    else:
        if not user.whitelisted:
            await message.answer("Тебя нет в вайтлисте!")

            return

    await message.answer("Добро пожаловать!", reply_markup=await menu_handler.get_node_keyboard(message.from_user,
                                                                                                menu_handler.root_node))
