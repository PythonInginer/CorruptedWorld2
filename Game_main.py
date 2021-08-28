import pygame
import pygame_gui
from data.system_dir.CONST import WIDTH, HEIGHT, FPS, PLAYERS, BULLETS, MAP_WH, GlobalFlags
from data.world_dir.load_map_optimiz import generate_level
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
detection = Detection(screen, GF, crafting)

map_conv = generate_level()
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
                detection.detect_keys(event.key, chat, player, inventory)  # передаём нажатые клавиши в обработчик
            if event.type == pygame.MOUSEBUTTONDOWN:
                detection.detect_mouse_keys(event.button, inventory, player)

        player.update()
        BULLETS.update(player)
        screen.blit(map_conv, (-player.move_x + (WIDTH - MAP_WH) / 2,
                               -player.move_y + (HEIGHT - MAP_WH) / 2))  # отображаем мир и двигаем его относительно нас
        PLAYERS.draw(screen)  # отрисовываем все спрайты
        BULLETS.draw(screen)

        detection.always_update(inventory, minimap, player)

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    game()
