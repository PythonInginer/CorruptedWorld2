import pygame
import pygame_gui
from data.system_dir.CONST import WIDTH, HEIGHT, FPS, PLAYERS, BULLETS, MAP_WH, GlobalFlags
from data.chat_dir.commands import set_player_pos
"""импорт классов"""
from data.chat_dir.chat import Chat
from data.player_dir.player import Player
from data.system_dir.minimap import Minimap
from data.system_dir.action_detector import Detection

pg = pygame
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
manager = pygame_gui.UIManager((WIDTH, HEIGHT))
pygame.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.MOUSEBUTTONDOWN])


fpsClock = pygame.time.Clock()

player = Player()
minimap = Minimap()
chat = Chat(manager, pg)
GF = GlobalFlags()
detection = Detection(screen, GF, player, chat)

set_player_pos(player, 0, 0)


def game():
    while GF.RUNNING:
        screen.fill((0, 0, 0))  # после этой строки пишем все обновления и отрисовки
        screen.set_colorkey((0, 0, 0))

        time_delta = fpsClock.tick(FPS) / 1000
        for event in pg.event.get():
            manager.process_events(event)
            if event.type == pg.QUIT:
                GF.RUNNING = False
            if event.type == pg.KEYDOWN:
                detection.get_keys(event.key)
            if event.type == pg.MOUSEBUTTONDOWN:
                detection.get_mouse_keys(event.button)

        detection.update_all()
        detection.draw_all()

        manager.update(time_delta)
        manager.draw_ui(screen)
        pg.display.flip()
    pg.quit()


if __name__ == "__main__":
    game()
