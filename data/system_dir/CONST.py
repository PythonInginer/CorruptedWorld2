import pygame


FPS = 60
WIDTH, HEIGHT = 1024, 600
TILES_COUNT_WH = int((len(open('data/world_dir/map.txt', 'r', encoding='utf8').readline()) // 2))

TILE_WH = 75
STACK = 4
MAP_WH = TILES_COUNT_WH * TILE_WH

BULLETS = pygame.sprite.Group()
PLAYERS = pygame.sprite.Group()
TILE_SPRITES = pygame.sprite.Group()
