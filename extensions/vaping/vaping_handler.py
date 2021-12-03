from datetime import datetime, timedelta
from typing import Optional

import pytz
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, User
from tortoise.exceptions import DoesNotExist
from tortoise.query_utils import Q

from api.state.state_result import StateResult
from api.state.state_with_buttons import StateWithButtons
from api.state.wrapped_states_group import WrappedStatesGroup
from bot import main
from extensions.vaping.models import VapingSettings, PuffEntry


def truncate_time(dt):
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


class DayState(StateWithButtons):
    async def send_state_message(self, chat_id: int):
        kb = InlineKeyboardMarkup()

        today = truncate_time(datetime.now())
        yesterday = today - timedelta(1)

        for button in self.buttons:
            if button.callback_data == "0":
                button_to_add = InlineKeyboardButton(text=f"{button.text} ({datetime.strftime(yesterday, '%d.%m')})",
                                                     callback_data=button.callback_data)
            else:
                button_to_add = InlineKeyboardButton(text=f"{button.text} ({datetime.strftime(today, '%d.%m')})",
                                                     callback_data=button.callback_data)

            kb.add(button_to_add)

        await main.bot.send_message(chat_id, text=self.message, reply_markup=kb)

    async def on_pre_state(self, message: Message, state: FSMContext) -> Optional[StateResult]:
        await self.on_state(message, state)

        day = (await state.get_data())["day"]

        now = truncate_time(datetime.now())
        date = now - timedelta(1) if day == 0 else now

        puff_entry = await PuffEntry.filter(user_id=message.from_user.id, date=pytz.utc.localize(date))

        return StateResult.FINISH if not len(puff_entry) else StateResult.COMPLETED


class PuffWriteForm(WrappedStatesGroup):
    day = DayState("За какое число записать затяжки?",
                   InlineKeyboardButton(text="📆 Вчера"),
                   InlineKeyboardButton(text="📆 Сегодня"), use_int_ids=True)
    action = StateWithButtons("За это число уже записаны затяжки! Что ты желаешь сделать:",
                              InlineKeyboardButton(text="➕ Прибавить"),
                              InlineKeyboardButton(text="❌✐ Перезаписать"), use_int_ids=True)


@PuffWriteForm.function()
async def puff_function(message: Message, user: User, puffs: int, day: int, action: int):
    now = truncate_time(datetime.now())
    date = now - timedelta(1) if day == 0 else now

    if action is None:
        await PuffEntry.create(user_id=user.id, puffs=puffs, date=date)

        await message.answer("Затяжки записаны!")
    else:
        puff_entry = (await PuffEntry.filter(user_id=user.id, date=pytz.utc.localize(date)))[0]

        puff_entry.puffs = puffs if action else puff_entry.puffs + puffs

        await puff_entry.save()

        await message.answer("Затяжки обновлены!")


@main.dp.message_handler(lambda message: message.text.isdigit())
async def vaping_handler(message: Message):
    if not (await VapingSettings.get_or_create(user_id=message.from_user.id))[0].vaping_activated:
        return

    value = int(message.text)

    if value < 0:
        return

    state_obj = PuffWriteForm.get_state_from_name(await PuffWriteForm.first())

    await Dispatcher.get_current().current_state().update_data(puffs=value)

    await state_obj.send_state_message(message.chat.id)
