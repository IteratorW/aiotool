from typing import Type

from api.settings import settings_handler
from api.settings.settings_category import SettingsCategory
from api.settings.settings_model import SettingsModel


def settings_descriptor(category_name: str, category_id: str, model: Type[SettingsModel]):
    def decorator(cls):
        members = [attr for attr in dir(cls) if not callable(getattr(cls, attr)) and not attr.startswith("__")]
        model_fields = model._meta.fields

        entries = []

        for member in members:
            if member not in model_fields:
                raise RuntimeError(f"Field {member} as described in settings could not be not found in model {model}")

            entry = getattr(cls, member)
            entry.db_field_name = member
            entry.db_field_type = model._meta.fields_map[entry.db_field_name].field_type

            if entry.db_field_type is bool:
                entry.name = entry.name[:1].lower() + entry.name[1:]

            entries.append(entry)

        settings_handler.items.append(SettingsCategory(category_name, category_id, entries, model))

        return cls

    return decorator
