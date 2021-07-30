import pygame
import pygame_gui
from player import Player
from CONST import WIDTH, HEIGHT, FPS, PLAYERS, TILE_SPRITES, BULLETS, TILES_COUNT_WH, TILE_WH, MAP_WH
from minimap import Minimap
from load_map_optimiz import generate_level
from commands import set_player_pos
from chat import Chat
from inventory import Inventory
from action_detector import Detection

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

fpsClock = pygame.time.Clock()
running = True

player = Player()
minimap = Minimap()
chat = Chat(manager)
detection = Detection()
inventory = Inventory(player.move_x,
                      player.move_y)

map_conv = generate_level()
PLAYERS.add(player)

set_player_pos(player, 0, 0)


def game():
    global running
    while running:
        screen.fill((0, 0, 0))  # после этой строки пишем все обновления и отрисовки

        time_delta = fpsClock.tick(FPS) / 1000
        for event in pygame.event.get():
            manager.process_events(event)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                detection.detect_keys(event.key, chat, player, inventory)  # передаём нажатые клавиши в обработчик
            if event.type == pygame.MOUSEBUTTONDOWN:
                detection.detect_mouse_keys(event.button, inventory)

        player.update()
        BULLETS.update()
        screen.blit(map_conv, (-player.move_x + (WIDTH - MAP_WH) / 2,
                               -player.move_y + (HEIGHT - MAP_WH) / 2))  # отображаем мир и двигаем его относительно нас
        PLAYERS.draw(screen)  # отрисовываем все спрайты
        BULLETS.draw(screen)

        detection.always_update(screen, inventory, minimap, player)

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()


game()
pygame.quit()
