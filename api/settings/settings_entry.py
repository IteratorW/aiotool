from typing import Optional

from aiogram.types import Message


class SettingsEntry:
    def __init__(self, name: str, message: str = None):
        self.name = name
        self.message = message

        self.db_field_name = None
        self.db_field_type = None

    @staticmethod
    async def process_value(message: Message) -> Optional[any]:
        return message.text

    def value_processor(self):
        def decorator(func):
            self.process_value = func

            return func

        return decorator
