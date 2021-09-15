import pygame
from data.system_dir.CONST import STACK


class Item(pygame.sprite.Sprite):
    def __init__(self, filename, item_id, item_type='item', stack=STACK):
        pygame.sprite.Sprite.__init__(self)

        """Работа со спрайтом"""
        self.im = pygame.image.load(filename)
        self.im = pygame.transform.scale(self.im, (50, 50))
        self.image = pygame.Surface((75, 75))
        self.image.set_colorkey((0, 0, 0))
        self.image.blit(self.im, (12, 12))
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

        """Отображение количиства предмета"""
        self.stack_style = pygame.font.SysFont('Verdana', 20)
        if self.max_count != 1:
            text = self.stack_style.render(f"{self.count}", False, (255, 255, 255))
            self.image.blit(text, (62, 52))

    def count_updater(self):
        if self.max_count != 1:
            self.image.fill((0, 0, 0))
            self.image.set_colorkey((0, 0, 0))
            self.image.blit(self.im, (12, 12))
            text = self.stack_style.render(f"{self.count}", False, (255, 255, 255))
            self.image.blit(text, (62, 52))

    def set_inventory_pos(self, x, y, shift_x, shift_y):  # функция для установления позиции в инвенторе
        self.rect.x = x * 75 + shift_x
        self.rect.y = y * 75 + shift_y

    def set_crafting_pos(self, x, y, cell_type):  # функция для установления позиции для крафта
        if cell_type == 1:
            self.rect.x = x
            self.rect.y = y
        elif cell_type == 2:
            self.rect.x = x
            self.rect.y = y

    def drop_moving(self):
        pass

    def moving(self):  # функция, которая позволяет двигать предмет мышью
        if self.mobility:
            x, y = pygame.mouse.get_pos()
            self.rect.x = x - 32
            self.rect.y = y - 32
