from typing import Callable

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.types import Message, ChatMember, User

from api.menu.decorators import aiotool_menu_node_handler
from api.menu.menu_node import MenuNode
from api.state.state_result import StateResult
from api.state.wrapped_state import WrappedState
from bot import main


class WrappedStatesGroup(StatesGroup):
    """
    Кастомный контейнер для стейтов, использующийся в обертке FSM аиограма.
    Управляет процессом перехода между стейтами а также регистрирует все хандлеры в aiogram для всех кастомных стейтов
    """

    on_finish_callback: Callable

    @classmethod
    def get_state_from_name(cls, state_name: str):
        for state in cls.states:
            if state.state == state_name:
                return state

        return None

    @classmethod
    async def finish(cls, message: Message, ctx: FSMContext):
        async with ctx.proxy() as proxy:
            data = proxy

        await ctx.finish()

        args = {}

        for arg in cls.on_finish_callback.__code__.co_varnames[:cls.on_finish_callback.__code__.co_argcount][1:]:
            args[arg] = data[arg] if arg in data else None

        del args["user"]

        user_id = ctx.user
        await cls.on_finish_callback(message, (await main.bot.get_chat_member(user_id, user_id)).user, **args)

    @classmethod
    async def proceed(cls, result: StateResult, message: Message, ctx: FSMContext):
        if result is StateResult.FINISH or (
                result is StateResult.COMPLETED and (await ctx.get_state()) == cls._states[-1].state):
            await cls.finish(message, ctx)
        elif result is StateResult.COMPLETED:
            next_state = cls.get_state_from_name(await cls.next())

            await next_state.send_state_message(message.chat.id)

    @classmethod
    def register_handlers(cls, on_finish_callback: Callable):
        cls.on_finish_callback = on_finish_callback

        for form_state in cls._states:
            if not isinstance(form_state, WrappedState):
                raise RuntimeError(f"State {form_state} is not subclass of CustomState, can't process")

            form_state.register_handler(cls)

    @classmethod
    def function(cls, node: MenuNode = None, parent_node: MenuNode = None):
        def decorator(func: Callable):
            cls.register_handlers(func)

            if node is not None:
                @aiotool_menu_node_handler(node, parent_node)
                async def handler(message: Message):
                    state_obj = cls.get_state_from_name(await cls.first())

                    await state_obj.send_state_message(message.chat.id)

            return func

        return decorator

