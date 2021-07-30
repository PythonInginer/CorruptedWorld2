from items import Item, MagicWand


def items_norm(name):
    if name in items_id:
        return Item(f'data/textures/items/{name}.png', items_id[name])


def items_weapon(name):
    if name in items_id:
        if name == 'magic_wand':
            return MagicWand(f'data/textures/items/{name}.png', items_id[name])


def get_key(value):
    for k, v in items_id.items():
        if v == value:
            return k


items_id = {'dirt': 1,
            'magic_wand': 2
            }
