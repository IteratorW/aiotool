from typing import Union

from aiogram.dispatcher.filters import Filter, BoundFilter
from aiogram.types import Message, CallbackQuery

from api.models import AiotoolUser
from bot import main


class AdminOnlyFilter(BoundFilter):
    key = "admin_only"

    def __init__(self, admin_only: bool):
        self.admin_only = admin_only

    async def check(self, obj: Union[Message, CallbackQuery]):
        if not self.admin_only:
            return True

        return (await AiotoolUser.get_or_create(user_id=obj.from_user.id))[0].admin


def bind_all():
    main.dp.bind_filter(AdminOnlyFilter)
