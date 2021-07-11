import pygame
import pygame_gui
from player import Player
from CONST import WIDTH, HEIGHT, FPS
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
inventory = Inventory()

map_conv, tiles_group = generate_level()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

set_player_pos(player, 2, 2)

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
    screen.blit(map_conv, (-player.move_x + WIDTH // 2,
                           -player.move_y + HEIGHT // 2))  # отображаем мир и двигаем его относительно нас
    all_sprites.draw(screen)  # отрисовываем все спрайты

    detection.always_update(screen, inventory, minimap, player)

    manager.update(time_delta)
    manager.draw_ui(screen)
    pygame.display.flip()
pygame.quit()
