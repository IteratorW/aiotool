from typing import Type, Optional

from aiogram.types import Message
from tortoise import fields, BaseDBAsyncClient, Model
from tortoise.signals import post_save, pre_save

from api.settings.decorators import settings_descriptor
from api.settings.settings_entry import SettingsEntry
from api.settings.settings_model import SettingsModel
from bot import main


def check_time(text: str):
    h_m = text.split(":")

    if len(h_m) < 2:
        return False

    try:
        h = int(h_m[0])
        m = int(h_m[1])
    except ValueError:
        return False

    return h in range(0, 24) and m in range(0, 60)


class VapingSettings(SettingsModel):
    vaping_activated = fields.BooleanField(default=False)
    notifications = fields.BooleanField(default=False)
    notifications_time = fields.TextField(default="00:00")


@post_save(VapingSettings)
async def vaping_post_save(
        sender: "Type[VapingSettings]",
        instance: VapingSettings,
        created: bool,
        using_db: "Optional[BaseDBAsyncClient]",
        update_fields: list[str],
) -> None:
    if update_fields is not None and "vaping_activated" in update_fields and instance.vaping_activated:
        await main.bot.send_message(instance.user_id, "Теперь ты сможешь записывать свои "
                                                      "затяжки каждый день, просто отправляй боту сообщение с "
                                                      "количеством затяжек.")


@settings_descriptor("😤 Вейпинг", "vaping_settings", VapingSettings)
class VapingSettingsDescriptor:
    vaping_activated = SettingsEntry("Вейпинг-функции")
    notifications = SettingsEntry("Напоминания записать затяжки")
    notifications_time = SettingsEntry("📅 Время напоминаний", message="Укажи время напоминаний (например 16:00 или "
                                                                            "00:00)")

    @staticmethod
    @notifications_time.value_processor()
    async def time_processor(message: Message):
        return message.text if check_time(message.text) else None


class PuffEntry(Model):
    user_id = fields.IntField()
    date = fields.DatetimeField()
    puffs = fields.IntField()

    class Meta:
        unique_together = (("user_id", "date"), )

