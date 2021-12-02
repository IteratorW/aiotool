from bot import main
from extensions.builtin.whitelist_middleware import WhitelistMiddleware
from . import administration
from . import settings
from . import whitelist
from .models import InviteEntry

main.dp.middleware.setup(WhitelistMiddleware())
