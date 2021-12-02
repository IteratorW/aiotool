from typing import Optional

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message, User

from api.menu.menu_node import MenuNode
from api.models import AiotoolUser
from bot import main

nodes: list[MenuNode] = []
parent_node_names: list[str] = []

root_node = MenuNode("root_node", "⬜ Главная")
nodes.append(root_node)


def add_node(menu_node: MenuNode, parent_node: MenuNode = None):
    menu_node.set_parent(root_node if parent_node is None else parent_node)

    nodes.append(menu_node)


def node_has_children(menu_node: MenuNode) -> bool:
    for node in nodes:
        if node.parent is not None and node.parent == menu_node.node_id:
            return True

    return False


def get_child_notes(menu_node: MenuNode):
    return [node for node in nodes if node.parent is not None and node.parent == menu_node.node_id]


def get_node_parent(menu_node: MenuNode) -> Optional[MenuNode]:
    if menu_node.parent is None:
        return None

    return next((x for x in nodes if x.node_id == menu_node.parent), None)


async def get_node_keyboard(user: User, menu_node: MenuNode):
    aiotool_user = (await AiotoolUser.get_or_create(user_id=user.id))[0]
    kb = ReplyKeyboardMarkup(resize_keyboard=False)

    parent_node = get_node_parent(menu_node)

    if parent_node is not None:
        kb.insert(KeyboardButton(text=parent_node.name))

        kb.row()

    for child_node in get_child_notes(menu_node):
        if not child_node.admin_only or (child_node.admin_only and aiotool_user.admin):
            kb.insert(KeyboardButton(text=child_node.name))

    return kb


@main.dp.message_handler(lambda message: message.text in parent_node_names)
async def parent_nodes_handler(message: Message):
    node = next((x for x in nodes if x.name == message.text), None)

    if node is None:
        return

    aiotool_user = (await AiotoolUser.get_or_create(user_id=message.from_user.id))[0]

    if node.admin_only and not aiotool_user.admin:
        return

    await message.reply(f"Категория - {node.name}", reply_markup=await get_node_keyboard(message.from_user, node))


def register_handlers():
    for node in nodes:
        if node_has_children(node):
            parent_node_names.append(node.name)
        else:
            node.register_handler()
