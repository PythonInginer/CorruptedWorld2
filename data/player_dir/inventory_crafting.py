import pygame
from data.system_dir.CONST import WIDTH, HEIGHT, CELL_WH
from data.system_dir.item_list import inventory_crafting_list, items_id
from data.system_dir.item_list import return_item


class Crafting:
    def __init__(self, screen, inventory):
        self.screen = screen
        self.inventory = inventory
        self.W = 200
        self.H = 245
        self.X = WIDTH - self.W - 20
        self.Y = 320
        self.craft_screen = pygame.Surface((self.W, self.H))
        self.craft_list_index = 0
        self.can_craft = []
        self.inventory_items_count = {}
        self.items_can_craft = pygame.sprite.Group()

    def update_all(self):
        self.draw_craft()
        self.screen.blit(self.craft_screen, (self.X, self.Y))

    def draw_craft(self):
        self.craft_screen.fill((0, 0, 0))
        self.craft_screen.set_colorkey((0, 0, 0))

        pygame.draw.rect(self.craft_screen, (255, 0, 0), (0, 0, self.W, self.H), 1)  # отладка(границы элемента)

        pygame.draw.rect(self.craft_screen, (255, 255, 255), (120, 10, 65, 65), 5)
        pygame.draw.rect(self.craft_screen, (255, 255, 255), (115, 85, 75, 75), 5)
        pygame.draw.rect(self.craft_screen, (255, 255, 255), (120, 170, 65, 65), 5)

        self.items_can_craft.draw(self.craft_screen)

    def update_can_craft(self):
        self.inventory_items_count = {}
        self.can_craft = []
        self.items_can_craft.empty()
        for y in range(len(self.inventory)):
            for x in range(len(self.inventory[y])):
                if self.inventory[y][x]:
                    if self.inventory[y][x].item_id in self.inventory_items_count:
                        self.inventory_items_count[self.inventory[y][x].item_id] += self.inventory[y][x].count
                    else:
                        self.inventory_items_count[self.inventory[y][x].item_id] = self.inventory[y][x].count

        for key in inventory_crafting_list.keys():
            can_craft_flag = True
            for index, count in inventory_crafting_list[key]:
                if index not in self.inventory_items_count.keys():
                    can_craft_flag = False
                    break
                else:
                    if count > self.inventory_items_count[index]:
                        can_craft_flag = False
                        break
            if can_craft_flag:
                self.can_craft.append(key)

        if len(self.can_craft) == 0:
            pass
        elif len(self.can_craft) == 1:
            item = return_item(items_id[self.can_craft[self.craft_list_index]])
            item.set_crafting_pos(115, 85, 1)
            self.items_can_craft.add(item)
        else:
            if self.craft_list_index == 0:
                item = return_item(items_id[self.can_craft[self.craft_list_index]])
                item.set_crafting_pos(115, 85, 1)
                self.items_can_craft.add(item)
                item = return_item(items_id[self.can_craft[self.craft_list_index + 1]])
                item.set_crafting_pos(120, 170, 2)
                self.items_can_craft.add(item)
            elif self.craft_list_index == len(self.can_craft) - 1:
                item = return_item(items_id[self.can_craft[self.craft_list_index - 1]])
                item.set_crafting_pos(120, 10, 2)
                self.items_can_craft.add(item)
                item = return_item(items_id[self.can_craft[self.craft_list_index]])
                item.set_crafting_pos(115, 85, 1)
                self.items_can_craft.add(item)
            else:
                item = return_item(items_id[self.can_craft[self.craft_list_index - 1]])
                item.set_crafting_pos(120, 10, 2)
                self.items_can_craft.add(item)
                item = return_item(items_id[self.can_craft[self.craft_list_index]])
                item.set_crafting_pos(115, 85, 1)
                self.items_can_craft.add(item)
                item = return_item(items_id[self.can_craft[self.craft_list_index + 1]])
                item.set_crafting_pos(120, 170, 2)
                self.items_can_craft.add(item)

    def update_craft_list(self, spin):
        self.items_can_craft.empty()
        if spin == 5:
            self.craft_list_index -= 1
        elif spin == 4:
            self.craft_list_index += 1

        if self.craft_list_index < 0:
            self.craft_list_index = 0
        elif self.craft_list_index >= len(self.can_craft):
            self.craft_list_index = len(self.can_craft) - 1

        if len(self.can_craft) == 0:
            pass
        elif len(self.can_craft) == 1:
            item = return_item(items_id[self.can_craft[self.craft_list_index]])
            item.set_crafting_pos(115, 85, 1)
            self.items_can_craft.add(item)
        else:
            if self.craft_list_index == 0:
                item = return_item(items_id[self.can_craft[self.craft_list_index]])
                item.set_crafting_pos(115, 85, 1)
                self.items_can_craft.add(item)
                item = return_item(items_id[self.can_craft[self.craft_list_index + 1]])
                item.set_crafting_pos(120, 170, 2)
                self.items_can_craft.add(item)
            elif self.craft_list_index == len(self.can_craft) - 1:
                item = return_item(items_id[self.can_craft[self.craft_list_index - 1]])
                item.set_crafting_pos(120, 10, 2)
                self.items_can_craft.add(item)
                item = return_item(items_id[self.can_craft[self.craft_list_index]])
                item.set_crafting_pos(115, 85, 1)
                self.items_can_craft.add(item)
            else:
                item = return_item(items_id[self.can_craft[self.craft_list_index - 1]])
                item.set_crafting_pos(120, 10, 2)
                self.items_can_craft.add(item)
                item = return_item(items_id[self.can_craft[self.craft_list_index]])
                item.set_crafting_pos(115, 85, 1)
                self.items_can_craft.add(item)
                item = return_item(items_id[self.can_craft[self.craft_list_index + 1]])
                item.set_crafting_pos(120, 170, 2)
                self.items_can_craft.add(item)

    def update_data(self, inventory):
        self.inventory = inventory
