from typing import Optional

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State
from aiogram.types import Message, InlineKeyboardMarkup

from bot import main
from api.state.state_result import StateResult


class WrappedState(State):
    """
    Базовый класс всех стейтов, учавствующих в нашей обертке над FSM аиограма.
    Теперь стейт служит не просто пунктом в форме, стейт это теперь самостоятельный объект, который сам обрабатывает
    полученные данные из сообщения.
    """

    def __init__(self, message: str, optional: bool = False):
        super().__init__()
        self.message = message
        self.optional = optional

    async def get_name(self, ctx: FSMContext) -> str:
        return (await ctx.get_state()).split(":")[-1]

    async def on_pre_state(self, message: Message, state: FSMContext) -> Optional[StateResult]:
        return await self.on_state(message, state)

    async def on_state(self, message: Message, state: FSMContext) -> Optional[StateResult]:
        pass

    async def send_state_message(self, chat_id: int):
        kb = None

        if self.optional:
            kb = InlineKeyboardMarkup().add(InlineKeyboardMarkup(text="⏩ Пропустить", callback_data="skip"))

        await main.bot.send_message(chat_id, text=self.message, reply_markup=kb)

    def __str__(self):
        return f"<CustomState '{self.state or ''}'>"
