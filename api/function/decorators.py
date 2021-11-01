import inspect
from typing import Callable

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.types import Message

from api import main
from api.state.custom_state import CustomState


def aiotool_function(form):
    def decorator(func: Callable):
        for state1 in form._states:
            if not isinstance(state1, CustomState):
                raise RuntimeError(f"State {state1} is not subclass of CustomState, can't process")

            @main.dp.message_handler(state=state1)
            async def on_prestate(message: Message, state: FSMContext):
                await state1.on_state(message, state)

                if state1 == form._states[-1]:
                    await func(message, state)

        return func

    return decorator
