# import pygame
# from pygame.locals import *
# import math
#
# # init stuff
# pygame.init()
# screen = pygame.display.set_mode((640, 480))
# clock = pygame.time.Clock()
# run = True
# orbs = []
# px = 1
# py = 1
# clock = pygame.time.Clock()
#
#
# # movement from one point to another
# def Move(t0, t1, psx, psy, speed):
#     global mx
#     global my
#
#     speed = speed
#
#     distance = [t0 - psx, t1 - psy]
#     norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
#     direction = [distance[0] / norm, distance[1] / norm]
#
#     bullet_vector = [direction[0] * speed, direction[1] * speed]
#     return bullet_vector
#
#
# # bullet class
# class Orb(object):
#     def __init__(self, posorg, posdest):
#         self.posx = posorg[0]
#         self.posy = posorg[1]
#         self.targx = posdest[0]
#         self.targy = posdest[1]
#         self.posorg = posorg
#         self.bullet_vector = Move(self.targx, self.targy, self.posx, self.posy, 20)
#
#     def update(self):
#         self.posx += self.bullet_vector[0]
#         self.posy += self.bullet_vector[1]
#         pygame.draw.circle(screen, (0, 0, 255), (int(self.posx), int(self.posy)), 5)
#
#
# # main loop
# while run:
#     screen.fill((220, 220, 220))
#     for o in orbs:
#         o.update()
#     (mx, my) = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
#
#     for e in pygame.event.get():
#         # quit on close button
#         if e.type == QUIT:
#             run = False
#         if e.type == MOUSEBUTTONDOWN:
#             if e.button == 1:
#                 orbs.append(Orb((px, py), (mx, my)))
#                 """px py это позиция игрока mx my позиция мыши"""
#     # player_dir movement
#     key = pygame.key.get_pressed()
#
#     if key[K_a]:
#         px -= 2
#     if key[K_d]:
#         px += 2
#     if key[K_w]:
#         py -= 2
#     if key[K_s]:
#         py += 2
#     clock.tick(60)
#     pygame.draw.circle(screen, (2, 150, 2), (int(px), int(py)), 30)
#     pygame.display.update()



import pygame as pg


pg.init()
screen = pg.display.set_mode((640, 480))
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)


def main():
    clock = pg.time.Clock()
    input_box1 = InputBox(100, 100, 140, 32)
    input_box2 = InputBox(100, 300, 140, 32)
    input_boxes = [input_box1, input_box2]
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
    pg.quit()