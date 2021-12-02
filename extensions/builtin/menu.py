from api.menu import menu_handler
from api.menu.menu_node import MenuNode

admin_node = MenuNode("administration", "✏️ Администрирование")
menu_handler.add_node(admin_node)
