from typing import Optional

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from api.state.auto.auto_state import AutoState
from api.state.wrapped_state import WrappedState
from api.state.state_result import StateResult


class AutoStringState(AutoState):
    """
    Этот автостейт просто возвращает все сообщение целиком
    """

    async def on_state(self, message: Message, state: FSMContext) -> Optional[StateResult]:
        await self.set_value(state, message.text)

        return StateResult.COMPLETED


class AutoIntState(AutoState):
    """
    Этот автостейт парсит число из всего сообщения
    """

    async def on_state(self, message: Message, state: FSMContext) -> Optional[StateResult]:
        try:
            await self.set_value(state, int(message.text))

            return StateResult.COMPLETED
        except ValueError:
            await message.reply("Долбоёб мне нужно число")

            return None
