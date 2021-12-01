from api.menu import menu_handler
from api.menu.menu_node import MenuNode


def aiotool_menu_node_handler(menu_node: MenuNode, parent_node: MenuNode = None):
    def decorator(func):
        menu_node.handler = func

        menu_handler.add_node(menu_node, parent_node)

        return func

    return decorator
