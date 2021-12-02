from typing import Type

from api.settings import settings_handler
from api.settings.settings_category import SettingsCategory
from api.settings.settings_model import SettingsModel


def settings_descriptor(category_name: str, category_id: str, model: Type[SettingsModel]):
    def decorator(cls):
        members = [attr for attr in dir(cls) if not callable(getattr(cls, attr)) and not attr.startswith("__")]
        model_fields = model._meta.fields

        entries = []

        for model_field in model_fields:
            if model_field not in members:
                print(f"Field {model_field} can not be found in settings descriptor {cls}")

                continue

            entry = getattr(cls, model_field)
            entry.db_field_name = model_field
            entry.db_field_type = model._meta.fields_map[entry.db_field_name].field_type

            if entry.db_field_type is bool:
                entry.name = entry.name[:1].lower() + entry.name[1:]

            entries.append(entry)

        settings_handler.items.append(SettingsCategory(category_name, category_id, entries, model))

        return cls

    return decorator
