from typing import Callable

from bot import main
from api.menu import menu_handler


"""
Декоратор, добавляющий новый пункт в меню и автоматически регистрирующий
простой хендлер на этот пункт.
"""


def aiotool_menu_entry(name: str):
    def decorator(func: Callable):

        menu_handler.items.append(name)

        main.dp.message_handler(lambda message: message.text == name)(func)

        return func

    return decorator
