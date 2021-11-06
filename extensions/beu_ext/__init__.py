from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from api.state.auto.auto_states import AutoIntState, AutoStringState
from api.state.wrapped_states_group import WrappedStatesGroup


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


@ProfileForm.function(menu="✍️ Заполнить профиль")
async def profile(message: Message, name: str, age: int, vape_model: str):
    await message.answer("Ты успешно заполнил профиль!")
    await message.answer(
        f"Имя: {name}\nВозраст: {age}\nМодель вейпа: {'нет дудки' if not vape_model else vape_model}")
