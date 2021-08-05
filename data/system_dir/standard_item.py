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
        self.item_type = item_type
        self.id = item_id
        self.max_count = stack

        """Системные параметры"""
        self.count = 1  # количесвто в слоте в данный момент

    def set_pos(self, x, y, shift_x, shift_y):  # функция для установления позиции в инвенторе
        self.rect.x = x * 75 + shift_x + 12
        self.rect.y = y * 75 + shift_y + 12

    def moving(self):  # функция, которая позволяет двигать предмет мышью
        if self.mobility:
            x, y = pygame.mouse.get_pos()
            self.rect.x = x - 12
            self.rect.y = y - 12
