from typing import Callable, Optional

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from api.state.wrapped_state import WrappedState
from api.state.state_result import StateResult


class AutoState(WrappedState):
    """
    Базовый класс всех автостейтов - стейтов, которые сами парсят сообщение в зависимости от их типа.
    """

    def __init__(self, message: str, optional: bool = False):
        super().__init__(message, optional)
        self.value = None

    async def on_pre_state(self, message: Message, state: FSMContext) -> Optional[StateResult]:
        result = await self.on_state(message, state)

        if result is not None:
            result = None if not (await self.check_value(self.value, message, state)) else result

        return result

    async def set_value(self, ctx: FSMContext, value: any):
        self.value = value

        state_name = await self.get_name(ctx)

        await ctx.update_data(**{state_name: value})

    async def get_value(self, ctx: FSMContext):
        async with ctx.proxy() as data:
            return data[await self.get_name(ctx)]

    @staticmethod
    async def check_value(value: any, message: Message, ctx: FSMContext) -> bool:
        return True

    def value_checker(self):
        def decorator(func: Callable):
            self.check_value = func

            return func

        return decorator
