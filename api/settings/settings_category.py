from typing import Type

from api.settings.settings_entry import SettingsEntry
from api.settings.settings_model import SettingsModel


class SettingsCategory:
    def __init__(self, name: str, category_id: str, entries: list[SettingsEntry], model: Type[SettingsModel]):
        self.name = name
        self.category_id = category_id
        self.entries = entries
        self.model = model
