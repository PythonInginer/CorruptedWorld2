import pygame

PG = pygame
PG.init()

FPS = 60
WIDTH, HEIGHT = 1920, 1080
TILES_COUNT_WH = int((len(open('data/world_dir/map.txt', 'r', encoding='utf8').readline()) // 2))

TILE_WH = 64
CELL_X = 8
CELL_Y = 4
CELL_WH = 64
STACK = 4
MAP_WH = TILES_COUNT_WH * TILE_WH

BULLETS = pygame.sprite.Group()
PLAYERS = pygame.sprite.Group()
DROP_ITEMS = pygame.sprite.Group()
TILE_SPRITES = pygame.sprite.Group()


class GlobalFlags:
    def __init__(self):
        self.RUNNING = True
