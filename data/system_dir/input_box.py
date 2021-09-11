from data.system_dir.CONST import PG


class InputBox:

    def __init__(self, x, y, w, h, txt_height, txt_color, bg_color, outline_color_T, outline_color_F, msim, text=''):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.txt_height = txt_height
        self.txt_color = txt_color
        self.bg_color = bg_color
        self.outline_color_T = outline_color_T
        self.outline_color_F = outline_color_F
        self.color = outline_color_T
        self.msim = msim
        self.text = text

        self.rect = PG.Rect(self.x, self.y, self.w, self.h)
        self.FONT = PG.font.Font(None, self.txt_height)
        self.txt_surface = self.FONT.render(text, True, self.txt_color)
        self.h_shift = (self.h - self.txt_surface.get_height()) // 2
        self.input_box_surface = PG.Surface((w, h))
        self.active = True

    def mouse_action(self, event):
        if self.rect.collidepoint(event.pos):
            self.active = not self.active
        else:
            self.active = False
        self.color = self.outline_color_T if self.active else self.outline_color_F

    def keyboard_action(self, event):
        keys = PG.key.get_pressed()
        if self.active:
            if keys[PG.K_BACKSPACE]:
                self.text = self.text[:-1]
            else:
                if event.type == PG.KEYDOWN and not keys[PG.K_RETURN] and len(self.text) < self.msim:
                    self.text += event.unicode

    def draw(self, screen):
        self.txt_surface = self.FONT.render(self.text, True, self.txt_color)
        w_shift = self.rect.w - self.txt_surface.get_width()
        w_shift = 5 if w_shift > 0 else w_shift - 10

        PG.draw.rect(self.input_box_surface, self.bg_color, (0, 0, self.w, self.h))
        self.input_box_surface.blit(self.txt_surface, (0 + w_shift, 0 + self.h_shift))
        PG.draw.rect(self.input_box_surface, self.color, (0, 0, self.w, self.h), 2)
        screen.blit(self.input_box_surface, (self.x, self.y))


"""
Как вызывать
************************************************************************************************************************
ibox1 = InputBox(x, y, w, h, txt_height, txt_color, bg_color, outline_color_T, outline_color_F, max_sim, text)
ibox1.handle_event(event)
ibox1.draw(screen)
************************************************************************************************************************
"""
