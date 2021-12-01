from tortoise import Model, fields


class AiotoolUser(Model):
    user_id = fields.IntField(pk=True)
    whitelisted = fields.BooleanField(default=False)
    admin = fields.BooleanField(default=False)
