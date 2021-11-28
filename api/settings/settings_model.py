from tortoise import fields, Model


class SettingsModel(Model):
    user_id = fields.IntField(pk=True)
