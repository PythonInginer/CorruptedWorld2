# import pygame
# import noise
#
# TILE_WH = 75
# TEXTURES = [
#     "dirt.jpg",
#             ]
#
#
# def load_texture(tx_name):
#     image = pygame.image.load(f'data/textures_dir/{tx_name}').convert()
#     image = image.convert_alpha()
#     image = pygame.transform.scale(image, (TILE_WH, TILE_WH))
#     return image

import noise
import numpy as np
from PIL import Image

shape = (512, 512)
scale = .5
octaves = 1
persistence = 0.5
lacunarity = 2.0
seed = 3  # np.random.randint(0, 100)

world = np.zeros(shape)

# make coordinate grid on [0,1]^2
x_idx = np.linspace(0, 1, shape[0])
y_idx = np.linspace(0, 1, shape[1])
world_x, world_y = np.meshgrid(x_idx, y_idx)

# apply perlin noise, instead of np.vectorize, consider using itertools.starmap()
world = np.vectorize(noise.pnoise2)(world_x / scale,
                                    world_y / scale,
                                    octaves=octaves,
                                    persistence=persistence,
                                    lacunarity=lacunarity,
                                    repeatx=512,
                                    repeaty=512,
                                    base=seed)

# here was the error: one needs to normalize the image first. Could be done without copying the array, though
img = np.floor((world + .5) * 255).astype(np.uint8)  # <- Normalize world_dir first
img = Image.fromarray(img, mode='L')
img.save('1.png')
img.show()

