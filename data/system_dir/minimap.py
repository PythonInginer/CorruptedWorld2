from data.system_dir.CONST import MAP_WH
import pygame


class Minimap:
    def __init__(self):
        self.W = 100  # ширина карты
        self.H = 100  # высота карты
        self.X = 0  # размещение слоя по X
        self.Y = 0  # размещение слоя по Y
        self.x_pos = 0
        self.y_pos = 0
        self.COLOR = (255, 255, 255)
        self.map_canvas = pygame.Surface((self.W, self.H))
        self.coordinates_style = pygame.font.Font(None, 20)

    def draw(self, main_canvas, player):
        self.x_pos = player.move_x  # получаем X игрока
        self.y_pos = player.move_y  # получаем Y игрока
        self.update()  # обновляем карту
        main_canvas.blit(self.map_canvas, (self.X, self.Y))  # отрисовываем карту
        main_canvas.blit(self.show_coordinates(), (self.X + 10, self.Y + self.H + 10))  # отрисовываем координаты

    def update(self):
        ppx = self.W / MAP_WH * self.x_pos + 50
        ppy = self.H / MAP_WH * self.y_pos + 50
        self.map_canvas.fill(self.COLOR)
        pygame.draw.rect(self.map_canvas, self.COLOR, (0, 0, self.W, self.H))
        pygame.draw.rect(self.map_canvas, (255, 0, 0), (ppx - 2, ppy - 2, 5, 5))

    def show_coordinates(self):
        text = self.coordinates_style.render(f"X:{self.x_pos // 75} Y:{self.y_pos // 75}", False, (0, 180, 0))
        return text
