import pygame
from data.system_dir.CONST import WIDTH, HEIGHT


class ExitToMenuBtn:
    def __init__(self, screen):
        self.screen = screen

        font = pygame.font.Font(None, 50)
        self.text = font.render("Выйти в меню", True, (255, 255, 255))

        self.X = WIDTH - self.text.get_width() - 20
        self.Y = HEIGHT - self.text.get_height() - 20

        self.exit_button = pygame.Rect(self.X, self.Y, self.text.get_width(), self.text.get_height())

    def draw(self):
        self.screen.blit(self.text, (self.X, self.Y))
