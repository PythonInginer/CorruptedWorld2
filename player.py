import pygame
from CONST import WIDTH, HEIGHT


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25, 25))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (WIDTH / 2, HEIGHT / 2)
        self.move_x = WIDTH / 2
        self.move_y = HEIGHT / 2
        self.can_move = True

    def update(self):
        keys = pygame.key.get_pressed()
        self.moving(keys)

    def moving(self, keys):
        if self.can_move:
            if keys[pygame.K_w]:
                self.move_y -= 5

            if keys[pygame.K_s]:
                self.move_y += 5

            if keys[pygame.K_a]:
                self.move_x -= 5

            if keys[pygame.K_d]:
                self.move_x += 5
