import pygame
from data.system_dir.CONST import STACK


class Item(pygame.sprite.Sprite):
    def __init__(self, filename, item_id, item_type='item', stack=STACK):
        pygame.sprite.Sprite.__init__(self)

        """Работа со спрайтом"""
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0

        """Настраиваемые параметры"""
        self.mobility = False
        self.drop = False
        self.item_type = item_type
        self.item_id = item_id
        self.max_count = stack

        """Системные параметры"""
        self.count = 1  # количесвто в слоте в данный момент

    def set_inventory_pos(self, x, y, shift_x, shift_y):  # функция для установления позиции в инвенторе
        self.rect.x = x * 75 + shift_x + 12
        self.rect.y = y * 75 + shift_y + 12

    def set_crafting_pos(self, x, y, cell_type):  # функция для установления позиции для крафта
        if cell_type == 1:
            self.rect.x = x + 12
            self.rect.y = y + 12
        elif cell_type == 2:
            self.rect.x = x + 7
            self.rect.y = y + 7

    def drop_moving(self):
        pass

    def moving(self):  # функция, которая позволяет двигать предмет мышью
        if self.mobility:
            x, y = pygame.mouse.get_pos()
            self.rect.x = x - 25
            self.rect.y = y - 25
