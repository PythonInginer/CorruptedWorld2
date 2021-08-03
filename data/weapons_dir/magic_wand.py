import pygame
from data.system_dir.CONST import BULLETS, WIDTH, HEIGHT


class MagicWand(pygame.sprite.Sprite):
    def __init__(self, filename, item_id, stack=1):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0
        self.bullet_speed = 5
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

    def fire(self, player):
        x_mouse, y_mouse = pygame.mouse.get_pos()
        x_mouse += player.move_x
        y_mouse += player.move_y
        BULLETS.add(Bullet('data/textures_dir/bullets/magic_wand_bullet.png',
                           x_mouse, y_mouse,
                           self.bullet_speed,
                           player))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, filename, x_mouse, y_mouse, speed, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()

        standard_x = player.move_x + WIDTH // 2 - 25
        standard_y = player.move_y + HEIGHT // 2 - 25

        self.speed = speed
        self.start_x, self.start_y = standard_x, standard_y
        self.fly_x, self.fly_y = standard_x, standard_y
        self.rect.x, self.rect.y = standard_x, standard_y
        self.range = 300

        self.step_x, self.step_y = Move_bullet(self.start_x, self.start_y,
                                               x_mouse, y_mouse,
                                               self.speed)

    def update(self, player):
        self.fly_x += self.step_x
        self.fly_y += self.step_y

        self.rect.x = -player.move_x + self.fly_x
        self.rect.y = -player.move_y + self.fly_y

        range_now = ((self.fly_x - self.start_x) ** 2 +
                     (self.fly_y - self.start_y) ** 2) ** 0.5
        if range_now >= self.range:
            self.kill()


def Move_bullet(player_x, player_y, mouse_x, mouse_y, speed):
    distance_x = mouse_x - player_x
    distance_y = mouse_y - player_y
    distance_to_target = (distance_x ** 2 + distance_y ** 2) ** 0.5
    direction_x = distance_x / distance_to_target
    direction_y = distance_y / distance_to_target
    step_x = direction_x * speed
    step_y = direction_y * speed

    return step_x, step_y
