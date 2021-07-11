import pygame
from random import randint

lvl_name = 'data/maps/map.txt'

pygame.init()
WIDTH, HEIGHT = 1920, 1080
TILE_WH = 75

screen = pygame.display.set_mode((WIDTH, HEIGHT))


class Tile(pygame.sprite.Sprite):  # создание тайла
    def __init__(self, tile_type, pos_x, pos_y, rotate, ghost_tiles_group, solid_tiles_group, max_x, max_y):
        super().__init__()

        im, ghost_solid = tile_images[tile_type]

        for i in range(randint(1, 3) if rotate == 4 else int(rotate)):
            im = pygame.transform.rotate(im, 90)
        if ghost_solid == 'ghost':
            ghost_tiles_group.add(self)
        elif ghost_solid == 'solid':
            solid_tiles_group.add(self)

        self.image = im
        self.rect = self.image.get_rect()

        self.field_x = TILE_WH * pos_x - TILE_WH * max_x // 2
        self.field_y = TILE_WH * pos_y - TILE_WH * max_y // 2

    def render(self, player_sprite):
        if abs(self.field_x - player_sprite.field_x) <= 1920 and \
                abs(self.field_y - player_sprite.field_y) <= 1080:
            self.rect.x = self.field_x - player_sprite.field_x + 950
            self.rect.y = self.field_y - player_sprite.field_y + 530


def load_image(name):  # рендерим изображение
    image = pygame.image.load(f'data/textures/{name}').convert()
    image = image.convert_alpha()
    image = pygame.transform.scale(image, (TILE_WH, TILE_WH))
    return image


def generate_level(level, ghost_tiles_group, solid_tiles_group, ms):  # рендерим уровень
    level = load_level(level)
    for y in range(len(level)):
        ms.append([])
        for x in range(len(level[y])):
            tile_type, rotate = level[y][x].split('_')
            tile = Tile(tile_type, x, y, int(rotate), ghost_tiles_group, solid_tiles_group, len(level[0]), len(level))
            ms[-1].append(tile)
    return ms


def load_level(filename):  # читаем уровень
    filename = "data/maps/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip().split() for line in mapFile]
    return level_map


tile_images = {
    'sandY1': (load_image('dirt.jpg'), 'ghost'),
    'DtGraB': (load_image('DirtGrassBot.jpg'), 'ghost'),
    'DtGraR': (load_image('DirtGrassRight.jpg'), 'ghost'),
    'DtGrBR': (load_image('DirtGrassBotRight.jpg'), 'ghost'),
    'DtGrTL': (load_image('DirtGrassTopLeft.jpg'), 'ghost'),
    'DtGrBL': (load_image('DirtGrassBotLeft.jpg'), 'ghost'),
    'DtGrTR': (load_image('DirtGrassTopRight.jpg'), 'ghost'),
    'InfCW1': (load_image('InfectCommonWater1.jpg'), 'ghost'),
    'InfCW2': (load_image('InfectCommonWater2.jpg'), 'ghost'),
    'InfSt1': (load_image('InfectStone1.jpg'), 'ghost'),
    'InfSt2': (load_image('InfectStone2.jpg'), 'ghost'),
    'InfSt3': (load_image('InfectStone3.jpg'), 'ghost'),
    'InfWt1': (load_image('InfectWater1.jpg'), 'solid'),
    'InfWt2': (load_image('InfectWater2.jpg'), 'solid'),
    'InfWt3': (load_image('InfectWater3.jpg'), 'solid'),
    'InfWt4': (load_image('InfectWater4.jpg'), 'solid'),
    'nigSt1': (load_image('nightStone1.jpg'), 'ghost'),
    'nigSt2': (load_image('nightStone2.jpg'), 'ghost'),
    'nigSt3': (load_image('nightStone3.jpg'), 'ghost'),
    'Stone1': (load_image('Stone1.jpg'), 'ghost'),
    'Stone2': (load_image('Stone2.jpg'), 'ghost'),
    'Stone3': (load_image('Stone3.jpg'), 'ghost'),
    'grass1': (load_image('grass1.jpg'), 'ghost'),
    'grass2': (load_image('grass2.jpg'), 'ghost'),
    'grass3': (load_image('grass3.jpg'), 'ghost'),
    'grass4': (load_image('grass4.jpg'), 'ghost'),
    'Water1': (load_image('Water1.jpg'), 'solid'),
    'Water2': (load_image('Water2.jpg'), 'solid'),
    'Water3': (load_image('Water3.jpg'), 'solid'),
    'Water4': (load_image('Water4.jpg'), 'solid'),
    'InTGrB': (load_image('infectTrueGrassB.jpg'), 'ghost'),
    'InTGBL': (load_image('infectTrueGrassBL.jpg'), 'ghost'),
    'InTGrL': (load_image('infectTrueGrassL.jpg'), 'ghost'),
    'InTGrR': (load_image('infectTrueGrassR.jpg'), 'ghost'),
    'InTGrT': (load_image('infectTrueGrassT.jpg'), 'ghost'),
    'InTGTR': (load_image('infectTrueGrassTR.jpg'), 'ghost'),

}
