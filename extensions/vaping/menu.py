from api.menu import menu_handler
from api.menu.menu_node import MenuNode

vaping_menu = MenuNode("vaping", "😤 Вейпинг")
menu_handler.add_node(vaping_menu)
