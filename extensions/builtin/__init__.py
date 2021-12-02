from bot import main
from extensions.builtin.whitelist_middleware import WhitelistMiddleware
from . import invites
from . import settings
from . import edit_user
from . import user_list
from . import start
from .models import InviteEntry

main.dp.middleware.setup(WhitelistMiddleware())
