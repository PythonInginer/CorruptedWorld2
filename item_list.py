from item import Item


def items(name):
    if name in items_id:
        return Item('data/textures/items/dirt.png', items_id[name])


def get_key(value):
    for k, v in items_id.items_group():
        if v == value:
            return k


items_id = {'dirt': 1,

            }
