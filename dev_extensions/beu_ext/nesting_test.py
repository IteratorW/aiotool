from api.menu import menu_handler
from api.menu.menu_node import MenuNode

prev_parent = None
for i in range(20):
    if i == 19:
        menu_handler.add_node(MenuNode("last_fucking_node", "Ура! Ты дошел до конца."), prev_parent)
    else:
        parent = MenuNode(f"n_test_{i}", f"Вложенное меню {i + 1}")

        menu_handler.add_node(parent, prev_parent)

        prev_parent = parent

