from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from api.menu.decorators import aiotool_menu_entry
from api.settings import settings_handler
from api.settings.settings_category import SettingsCategory
from bot import main

field_types_messages = {
    int: "Укажи число для этой настройки",
    str: "Укажи текст для этой настройки",
    float: "Укажи число с плавающей точкой для этой настройки"
}


def get_settings_keyboard():
    kb = InlineKeyboardMarkup()

    for category in settings_handler.items:
        kb.add(InlineKeyboardButton(text=category.name, callback_data=f"settings|{category.category_id}"))

    return kb


async def get_category_keyboard(category: SettingsCategory, user_id: int):
    kb = InlineKeyboardMarkup()

    for entry in category.entries:
        text = entry.name

        is_boolean = entry.db_field_type is bool

        if is_boolean:
            enabled = getattr((await category.model.get_or_create(user_id=user_id))[0], entry.db_field_name)

            text = f"{'🔴 Выключить' if enabled else '🟢 Включить'} {text}"

        kb.add(InlineKeyboardButton(text=text,
                                    callback_data=f"category|{category.category_id}|{entry.db_field_name}{'|bool' if is_boolean else ''}"))

    return kb


def get_category_from_name(name: str):
    for cat in settings_handler.items:
        if cat.category_id == name:
            return cat


class SettingsForm(StatesGroup):
    value = State()


@main.dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("category|"))
async def category_callback_handler(callback_query: CallbackQuery):
    await main.bot.answer_callback_query(callback_query.id)

    data = callback_query.data.split("|")

    if len(data) < 3:
        return

    category = get_category_from_name(data[1])
    entry = None

    for entr in category.entries:
        if entr.db_field_name == data[2]:
            entry = entr
            break

    if entry is None:
        await callback_query.message.reply("Неизвестная настройка!")

        return

    if len(data) > 3 and data[3] == "bool":
        inst = (await category.model.get_or_create(user_id=callback_query.from_user.id))[0]

        enabled = getattr(inst, entry.db_field_name)

        await inst.update_from_dict({entry.db_field_name: not enabled})
        await inst.save()

        await callback_query.message.reply(f"Ты {'выключил' if enabled else 'включил'} {entry.name}")
    else:
        if entry.message is None:
            try:
                text = field_types_messages[entry.db_field_type]
            except KeyError:
                text = "Укажи значение для этой настройки!"
        else:
            text = entry.message

        await callback_query.message.reply(text)

        await SettingsForm.value.set()
        state = Dispatcher.get_current().current_state()

        await state.update_data(setting=callback_query.data)


@main.dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("settings|"))
async def settings_callback_handler(callback_query: CallbackQuery):
    await main.bot.answer_callback_query(callback_query.id)

    category = get_category_from_name(callback_query.data.split("|")[-1])

    if category is None:
        await callback_query.message.reply("Неизвестная категория!")

        return

    await callback_query.message.reply(f"Настройки - {category.name}", reply_markup=await get_category_keyboard(category,
                                                                                                          callback_query.
                                                                                                          from_user.id))


@main.dp.message_handler(state=SettingsForm.value)
async def settings_state_handler(message: Message, state: FSMContext):
    data = (await state.get_data())["setting"].split("|")

    if len(data) != 3:
        return

    category = get_category_from_name(data[1])
    entry = None

    for entr in category.entries:
        if entr.db_field_name == data[2]:
            entry = entr
            break

    if entry is None:
        return

    if entry.message is None:
        try:
            invalid_text = f"\n{field_types_messages[entry.db_field_type]}"
        except KeyError:
            invalid_text = ""
    else:
        invalid_text = f"\n{entry.message}"

    value = await entry.process_value(message)

    if value is None:
        await message.reply(f"Неверное значение!\n{invalid_text}")

        return

    inst = (await category.model.get_or_create(user_id=message.from_user.id))[0]

    try:
        await inst.update_from_dict({entry.db_field_name: message.text})
    except ValueError:
        await message.reply(f"Неверное значение!\n{invalid_text}")

        return

    await inst.save()

    await message.reply("Значение установлено!")

    await state.finish()


@aiotool_menu_entry("⚙️ Настройки")
async def handler(message: Message):
    await message.reply("Категории настроек:", reply_markup=get_settings_keyboard())
