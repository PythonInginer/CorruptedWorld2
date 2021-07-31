import pygame
from pygame.locals import *
import math

# init stuff
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
run = True
orbs = []
px = 1
py = 1
clock = pygame.time.Clock()


# movement from one point to another
def Move(t0, t1, psx, psy, speed):
    global mx
    global my

    speed = speed

    distance = [t0 - psx, t1 - psy]
    norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
    direction = [distance[0] / norm, distance[1] / norm]

    bullet_vector = [direction[0] * speed, direction[1] * speed]
    return bullet_vector


# bullet class
class Orb(object):
    def __init__(self, posorg, posdest):
        self.posx = posorg[0]
        self.posy = posorg[1]
        self.targ = posdest
        self.posorg = posorg
        self.bullet_vector = Move(self.targ[0], self.targ[1], self.posx, self.posy, 20)

    def update(self):
        self.posx += self.bullet_vector[0]
        self.posy += self.bullet_vector[1]
        pygame.draw.circle(screen, (0, 0, 255), (int(self.posx), int(self.posy)), 5)


# main loop
while run:
    screen.fill((220, 220, 220))
    for o in orbs:
        o.update()
    (mx, my) = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

    for e in pygame.event.get():
        # quit on close button
        if e.type == QUIT:
            run = False
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                orbs.append(Orb((px, py), (mx, my)))
    # player_dir movement
    key = pygame.key.get_pressed()

    if key[K_a]:
        px -= 2
    if key[K_d]:
        px += 2
    if key[K_w]:
        py -= 2
    if key[K_s]:
        py += 2
    clock.tick(60)
    pygame.draw.circle(screen, (2, 150, 2), (int(px), int(py)), 30)
    pygame.display.update()
