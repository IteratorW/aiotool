from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardButton

from api.state.auto.auto_states import AutoIntState, AutoStringState
from api.state.state_with_buttons import StateWithButtons
from api.state.wrapped_states_group import WrappedStatesGroup

from . import test_fn

vaping_times = ["меньше года", "1 год", "больше года", "больше двух лет"]


class ProfileForm(WrappedStatesGroup):
    name = AutoStringState("Как тебя зовут?")
    age = AutoIntState("Сколько тебе лет?")

    @staticmethod
    @age.value_checker()
    async def age_checker(value: any, message: Message, ctx: FSMContext):
        if value is not None and value < 18:
            await message.reply("Тебе еще нет 18, пиздюк!")

            return False

        return True

    vape_model = AutoStringState("Укажи модель своего вейпа или пропусти, если он у тебя, по какой-то причине, "
                                 "отсутствует.", optional=True)
    vaping_time = StateWithButtons("Укажи сколько ты уже паришь",
                                   InlineKeyboardButton(text="🟢 Меньше года"),
                                   InlineKeyboardButton(text="🟡 Год"),
                                   InlineKeyboardButton(text="🟥 Больше года"),
                                   InlineKeyboardButton(text="⚰️ Больше двух лет"), use_int_ids=True)


@ProfileForm.function(menu="✍️ Заполнить профиль")
async def profile(message: Message, name: str, age: int, vape_model: str, vaping_time: int):
    await message.answer("Ты успешно заполнил профиль!")
    await message.answer(
        f"Имя: {name}\nВозраст: {age}\nСтаж парения: {vaping_times[vaping_time]}\nМодель вейпа: {'нет дудки' if not vape_model else vape_model}")
