import pygame
import pygame_gui
from data.system_dir.CONST import WIDTH, HEIGHT, FPS, PLAYERS, BULLETS, MAP_WH, GlobalFlags
from data.chat_dir.commands import set_player_pos
"""импорт классов"""
from data.chat_dir.chat import Chat
from data.player_dir.player import Player
from data.system_dir.minimap import Minimap
from data.player_dir.inventory import Inventory
from data.system_dir.action_detector import Detection
from data.player_dir.inventory_crafting import Crafting


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

fpsClock = pygame.time.Clock()

player = Player()
minimap = Minimap()
chat = Chat(manager)
GF = GlobalFlags()
inventory = Inventory()
crafting = Crafting(screen, inventory.inventory_cells)
detection = Detection(screen, GF, player, inventory, crafting, chat)

PLAYERS.add(player)

set_player_pos(player, 0, 0)


def game():
    while GF.RUNNING:
        screen.fill((0, 0, 0))  # после этой строки пишем все обновления и отрисовки

        time_delta = fpsClock.tick(FPS) / 1000
        for event in pygame.event.get():
            manager.process_events(event)
            if event.type == pygame.QUIT:
                GF.RUNNING = False
            if event.type == pygame.KEYDOWN:
                detection.get_keys(event.key)
            if event.type == pygame.MOUSEBUTTONDOWN:
                detection.get_mouse_keys(event.button)

        detection.update_all()
        detection.draw_all()
        detection.always_update()

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    game()
