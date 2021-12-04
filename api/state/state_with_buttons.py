from typing import Type, TYPE_CHECKING, Optional

from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message

from api.state.state_result import StateResult
from api.state.wrapped_state import WrappedState
from bot import main

if TYPE_CHECKING:
    from api.state.wrapped_states_group import WrappedStatesGroup


class StateWithButtons(WrappedState):
    """
    Данный стейт вместо того чтобы брать данные из сообщения отправляет пользователю
    указанные кнопки и возвращает callback_id нажатой. (или индекс кнопки начиная с 0 при указанном
    аргументе use_int_ids)
    """

    def __init__(self, message: str, *buttons: InlineKeyboardButton, optional: bool = False, use_int_ids: bool = False):
        super().__init__(message, optional)

        self.buttons = buttons
        self.use_int_ids = use_int_ids

        if not self.use_int_ids:
            self.callback_ids = [button.callback_data for button in self.buttons]
        else:
            i = 0

            for button in self.buttons:
                button.callback_data = str(i)

                i += 1

    # идеальный пример показывающий пределы текущей обертки над стейтами - метод on_state предусматривает только
    # обработку данных из сообщения, по этому приходится обрабатывать значения из кнопок в самом хандлере
    # (что неправильно)
    async def on_state(self, message: Message, state: FSMContext) -> Optional[StateResult]:
        return StateResult.COMPLETED

    def register_handler(self, form: Type["WrappedStatesGroup"]):
        @main.dp.callback_query_handler(state=self)
        async def state_cb(query: CallbackQuery, state: FSMContext):
            await main.bot.answer_callback_query(query.id)

            if self.optional and query.data == "skip":
                await main.bot.answer_callback_query(query.id)

                await form.proceed(StateResult.COMPLETED, query.message, state)

                return

            if self.use_int_ids:
                try:
                    value = int(query.data)

                    if value not in range(0, len(self.buttons)):
                        return
                except ValueError:
                    return
            else:
                value = query.data

                if value not in self.callback_ids:
                    return

            await state.update_data(**{await self.get_name(state): value})

            result = await self.on_pre_state(query, state)

            await form.proceed(result, query.message, state)

    async def send_state_message(self, chat_id: int):
        kb = InlineKeyboardMarkup()

        if self.optional:
            kb.add(InlineKeyboardButton(text="⏩ Пропустить", callback_data="skip"))

        for button in self.buttons:
            kb.add(button)

        await main.bot.send_message(chat_id, text=self.message, reply_markup=kb)
