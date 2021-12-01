from tortoise import Model, fields


class InviteEntry(Model):
    code = fields.TextField(pk=True)
    flag = fields.SmallIntField(default=0)
    used = fields.BooleanField(default=False)
