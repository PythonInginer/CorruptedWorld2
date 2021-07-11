import pygame
from CONST import WIDTH, HEIGHT, TILE_WH


class Tile(pygame.sprite.Sprite):  # создание тайла
    def __init__(self, pos_x, pos_y, im):
        pygame.sprite.Sprite.__init__(self)
        self.image = im
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y


lvl_name = 'data/map.txt'


def load_image(name):  # рендерим изображение
    image = pygame.image.load(f'data/textures/{name}').convert()
    image = image.convert_alpha()
    image = pygame.transform.scale(image, (TILE_WH, TILE_WH))
    return image


def load_level(filename):  # читаем уровень из файла
    with open(filename, 'r') as mapFile:
        level_map = [line.strip().split() for line in mapFile]
    return level_map, len(level_map[0]), len(level_map)


def generate_level():  # выставляем тайлы на холст
    level_map, X, Y = load_level(lvl_name)
    world_map_conv = pygame.Surface((75 * X, 75 * Y))
    tiles_sprites = pygame.sprite.Group()
    for y in range(len(level_map)):
        for x in range(len(level_map[y])):
            tiles_sprites.add(Tile(75 * x, 75 * y, load_image(tile_images[level_map[y][x]][0])))
    tiles_sprites.draw(world_map_conv)
    return world_map_conv, tiles_sprites


tile_images = {
    'd': ('dirt.jpg', 'ghost')
}

"""   generate_level является конечной функцией   """
