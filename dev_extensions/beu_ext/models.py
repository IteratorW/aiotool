from aiogram.types import Message
from tortoise import fields

from api.settings.decorators import settings_descriptor
from api.settings.settings_entry import SettingsEntry
from api.settings.settings_model import SettingsModel


class TestSettings(SettingsModel):
    test_string = fields.TextField(default="anus")
    test_bool = fields.BooleanField(default=True)
    test_int = fields.IntField(default=228)


@settings_descriptor("🛠️ Тестовые настройки", "testsettings", TestSettings)
class TestSettingsDescriptor:
    test_string = SettingsEntry("Тестовая строка")
    test_bool = SettingsEntry("Тестовое булевое значение")
    test_int = SettingsEntry("Тестовое число", message="Укажи число не больше 50!")

    @staticmethod
    @test_int.value_processor()
    async def test_int_processor(message: Message):
        try:
            value = int(message.text)
        except ValueError:
            return message.text

        if value > 50:
            return None

        return message.text
