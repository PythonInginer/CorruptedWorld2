from data.system_dir.item_list import return_item


def set_player_pos(player, x, y):
    player.move_x, player.move_y = x * 75, y * 75


def give_item(inventory, item_name, count):
    for i in range(count):
        inventory.append_item(return_item(item_name))


def inventory_clear(inventory):
    inventory.inventory_clear()
