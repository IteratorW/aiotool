from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

numbers = {
    1: "1️⃣",
    2: "2️⃣",
    3: "3️⃣",
    4: "4️⃣",
    5: "5️⃣",
    6: "6️⃣",
    7: "7️⃣",
    8: "8️⃣",
    9: "9️⃣",
    0: "0️⃣"
}


def get_markup() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()

    for i in range(1, 10):
        kb.insert(InlineKeyboardButton(numbers[i], callback_data=f"keypad_num_{i}"))

    kb.insert(InlineKeyboardButton("❌", callback_data="keypad_erase"))
    kb.insert(InlineKeyboardButton(numbers[0], callback_data="keypad_num_0"))
    kb.insert(InlineKeyboardButton("✅", callback_data="keypad_submit"))

    return kb
