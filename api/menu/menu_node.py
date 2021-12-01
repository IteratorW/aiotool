from aiogram.types import Message

from bot import main


class MenuNode:
    def __init__(self, node_id: str, name: str, admin_only: bool = False):
        self.node_id = node_id
        self.name = name
        self.admin_only = admin_only

        self.parent = None

    def set_parent(self, parent_node: "MenuNode"):
        self.parent = parent_node.node_id

    def register_handler(self):
        main.dp.message_handler(lambda message: message.text == self.name)(self.handler)

    @staticmethod
    async def handler(message: Message):
        pass
