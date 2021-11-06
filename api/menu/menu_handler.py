from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

items: list[str] = []

"""
Здесь создается разметка главного меню. Пока что все в базовом состоянии,
позже будет разделение на категории, страницы, etc.
"""


def get_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    i = 0

    for item in items:
        keyboard.insert(KeyboardButton(item))

        i += 1

        if i == 3:
            keyboard.row()
            i = 0

    return keyboard
