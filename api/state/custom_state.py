from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State
from aiogram.types import Message


class CustomState(State):
    @staticmethod
    async def on_state(message: Message, state: FSMContext):
        pass
