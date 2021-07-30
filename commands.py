from item_list import items_norm, items_weapon


def set_player_pos(player, x, y):
    player.move_x, player.move_y = x * 75, y * 75


def give_item(inventory, item_type, item_name, count):
    if item_type == 'item':
        for i in range(count):
            inventory.append_item(items_norm(item_name))
    elif item_type == 'weapon':
        for i in range(count):
            inventory.append_item(items_weapon(item_name))


def inventory_clear(inventory):
    inventory.inventory_clear()
