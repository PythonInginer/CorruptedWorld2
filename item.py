import pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, filename, item_id):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0
        self.mobility = False
        self.count = 1
        self.id = item_id

    def set_pos(self, x, y, shift_x, shift_y):
        self.rect.x = x * 75 + shift_x + 12
        self.rect.y = y * 75 + shift_y + 12

    def moving(self):
        if self.mobility:
            x, y = pygame.mouse.get_pos()
            self.rect.x = x - 12
            self.rect.y = y - 12
