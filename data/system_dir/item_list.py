#  Импорт предметов
from data.items_dir.dirt import Dirt
# Импорт оружий
from data.weapons_dir.magic_wand import MagicWand


def return_item(name):
    if name == 'dirt':
        return Dirt()
    elif name == 'magic_wand':
        return MagicWand()


items_id = {
    1: "dirt",
    2: "magic_wand"
}

# ключ-то, что крафтим | список[0]-индекс предмета | список[1]-количество предмета
inventory_crafting_list = {
    2: [[1, 5]],
    1: [[1, 1]]
}
