import git
from aiogram.types import Message, ParseMode
from aiogram.utils.markdown import hbold
from git import InvalidGitRepositoryError

from api.menu.decorators import aiotool_menu_node_handler
from api.menu.menu_node import MenuNode


def get_version():
    try:
        repo = git.Repo(search_parent_directories=True)
    except InvalidGitRepositoryError:
        return None

    version = next((tag for tag in repo.tags if tag.commit == repo.head.commit), None)

    if version is None:
        version = repo.git.rev_parse(repo.head.commit.hexsha, short=7)

    del repo

    return version


current_version = get_version()


@aiotool_menu_node_handler(MenuNode("bot_info", "ℹ️ Информация о боте"))
async def info_handler(message: Message):
    await message.reply(f"""
aiotool
Версия: {hbold(current_version if current_version is not None else "Неизвестно")}
Авторы: {hbold("Iterator, Danbonus")}
""", parse_mode=ParseMode.HTML)
