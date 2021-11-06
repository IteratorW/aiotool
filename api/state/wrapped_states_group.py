from typing import Callable

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.types import Message, CallbackQuery

from bot import main
from api.menu.decorators import aiotool_menu_entry
from api.state.wrapped_state import WrappedState
from api.state.state_result import StateResult


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

        for arg in cls.on_finish_callback.__code__.co_varnames[1:]:
            args[arg] = data[arg] if arg in data else None

        await cls.on_finish_callback(message, **args)

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

            if form_state.optional:
                @main.dp.callback_query_handler(lambda c: c.data == "skip", state=form_state)
                async def state_cb(query: CallbackQuery, state: FSMContext):
                    await main.bot.answer_callback_query(query.id)

                    await cls.proceed(StateResult.COMPLETED, query.message, state)

            # Здесь говнокод. Регистрация хандлеров происходит в цикле чтобы зарегестрировать хандлеры на каждый стейт.
            # В идеале лучше было бы найти способ зарегестрировать один хандлер на одну группу стейтов, но я не ебу как.
            # noinspection PyProtectedMember
            @main.dp.message_handler(state=form_state)
            async def handler(message: Message, state: FSMContext):
                state_obj = cls.get_state_from_name(await state.get_state())

                result = await state_obj.on_pre_state(message, state)

                await cls.proceed(result, message, state)

    @classmethod
    def function(cls, menu: str = None):
        def decorator(func: Callable):
            cls.register_handlers(func)

            if menu is not None:
                @aiotool_menu_entry(menu)
                async def handler(message: Message):
                    state_obj = cls.get_state_from_name(await cls.first())

                    await state_obj.send_state_message(message.chat.id)

            return func

        return decorator

