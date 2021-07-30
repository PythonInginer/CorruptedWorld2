import pygame
from CONST import STACK, BULLETS, WIDTH, HEIGHT


class Item(pygame.sprite.Sprite):
    def __init__(self, filename, item_id, stack=STACK):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0
        self.mobility = False
        self.item_type = 'item'
        self.count = 1
        self.max_count = stack
        self.id = item_id

    def set_pos(self, x, y, shift_x, shift_y):
        self.rect.x = x * 75 + shift_x + 12
        self.rect.y = y * 75 + shift_y + 12

    def moving(self):
        if self.mobility:
            x, y = pygame.mouse.get_pos()
            self.rect.x = x - 12
            self.rect.y = y - 12


class MagicWand(pygame.sprite.Sprite):
    def __init__(self, filename, item_id, stack=1):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0
        self.mobility = False
        self.item_type = 'weapon'
        self.count = 1
        self.max_count = stack
        self.id = item_id

    def set_pos(self, x, y, shift_x, shift_y):
        self.rect.x = x * 75 + shift_x + 12
        self.rect.y = y * 75 + shift_y + 12

    def moving(self):
        if self.mobility:
            x, y = pygame.mouse.get_pos()
            self.rect.x = x - 12
            self.rect.y = y - 12

    def fire(self, x_player, y_player):
        x_mouse, y_mouse = pygame.mouse.get_pos()
        BULLETS.add(Bullet('data/textures/bullets/magic_wand_bullet.png',
                           x_player, y_player,
                           x_mouse, y_mouse))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, filename, x_player, y_player, x_mouse, y_mouse):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.start_x, self.start_y = x_player + WIDTH // 2 - 25, y_player + HEIGHT // 2 - 25
        self.rect.x, self.rect.y = self.start_x, self.start_y
        self.range = 500

        self.bullet_vector = Move_bullet(self.start_x, self.start_y,
                                         x_mouse, y_mouse,
                                         10)

    def update(self):
        self.rect.x -= self.bullet_vector[0]
        self.rect.y -= self.bullet_vector[1]
        range_now = ((self.rect.x - self.start_x) ** 2 +
                     (self.rect.y - self.start_y) ** 2) ** 0.5
        if range_now >= self.range:
            self.kill()
        print(self.rect.x, self.rect.y, range_now)


def Move_bullet(t0, t1, psx, psy, speed):
    speed = speed

    distance = [t0 - psx, t1 - psy]
    norm = (distance[0] ** 2 + distance[1] ** 2) ** 0.5
    direction = [distance[0] / norm, distance[1] / norm]

    bullet_vector = [direction[0] * speed, direction[1] * speed]
    return bullet_vector
