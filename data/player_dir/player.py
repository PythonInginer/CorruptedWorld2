import pygame
from data.system_dir.CONST import WIDTH, HEIGHT


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25, 25))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (WIDTH / 2 - 12, HEIGHT / 2 - 12)
        self.move_x = 0
        self.move_y = 0
        self.can_move = True

    def player_class(self):
        pass

    def update(self):  # обновление всех действий связанных с игроком
        keys = pygame.key.get_pressed()
        self.moving(keys)

    def moving(self, keys):  # движение
        if self.can_move:
            if keys[pygame.K_w]:
                self.move_y -= 5

            if keys[pygame.K_s]:
                self.move_y += 5

            if keys[pygame.K_a]:
                self.move_x -= 5

            if keys[pygame.K_d]:
                self.move_x += 5
