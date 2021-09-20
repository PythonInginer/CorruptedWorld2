import pygame
from data.system_dir.CONST import STACK, WIDTH, HEIGHT


class Item(pygame.sprite.Sprite):
    def __init__(self, filename, item_id, item_type='item', stack=STACK, stacking=True):
        pygame.sprite.Sprite.__init__(self)

        """Работа со спрайтом"""
        self.im = pygame.image.load(filename)
        self.im = pygame.transform.scale(self.im, (50, 50))
        self.image = pygame.Surface((75, 75))
        self.image.set_colorkey((0, 0, 0))
        self.image.blit(self.im, (12, 12))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0
        self.dropX, self.dropY = 0, 0

        """Настраиваемые параметры"""
        self.item_type = item_type  # тип предмета
        self.item_id = item_id  # id предмета
        self.max_count = stack  # максимальное количество предмета
        self.stacking = stacking  # может ли предмет стакаться

        """Стационарные параметры"""
        self.count = 1  # количесвто в слоте в данный момент
        self.mobility = False
        self.drop = False

        """Отображение количиства предмета"""
        self.stack_style = pygame.font.SysFont('Verdana', 20)

    def count_updater(self):
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.image.blit(self.im, (12, 12))
        if not self.drop:
            if self.stacking:
                if self.max_count != 1:
                    text = self.stack_style.render(f"{self.count}", False, (255, 255, 255))
                    self.image.blit(text, (50, 50))

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

    def set_drop_pos(self, x, y):
        self.dropX = x - 37
        self.dropY = y - 37

    def moving(self):  # функция, которая позволяет двигать предмет мышью
        if self.mobility:
            x, y = pygame.mouse.get_pos()
            self.rect.x = x - 32
            self.rect.y = y - 32

    def update(self, playerX, playerY):
        self.rect.x = self.dropX - playerX + WIDTH // 2
        self.rect.y = self.dropY - playerY + HEIGHT // 2
