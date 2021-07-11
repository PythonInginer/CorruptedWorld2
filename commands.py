from item_list import items


def set_player_pos(player, x, y):
    player.move_x, player.move_y = x * 75, y * 75


def give_item(inventory, item_name, count):
    for i in range(count):
        inventory.append_item(items(item_name))


def inventory_clear(inventory):
    inventory.inventory_clear()
