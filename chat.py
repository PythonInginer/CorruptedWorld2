import pygame_gui
import pygame
import commands
from CONST import WIDTH, HEIGHT


class Chat:
    def __init__(self, manager):
        W = 500
        H = 40
        self.manager = manager
        self.chat = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((WIDTH - W - 20, HEIGHT - H - 10), (W, H)),
            manager=self.manager
        )
        self.hide_chat()

    def show_chat(self):
        self.chat.show()

    def hide_chat(self):
        self.chat.set_text('')
        self.chat.hide()

    def update(self, player, inventory):
        text = self.chat.get_text()
        if text != '':
            if text[0] == '/':
                text = text.split()
                if text[0][1:] == 'tp':
                    commands.set_player_pos(player, int(text[1]), int(text[2]))
                if text[0][1:] == 'give':
                    commands.give_item(inventory, text[1], int(text[2]))
                if text[0][1:] == 'inventory_clear':
                    commands.inventory_clear(inventory)
            else:
                pass

    def open_close_chat(self, chat_detect, player, inventory):
        if chat_detect:
            self.show_chat()
        else:
            self.update(player, inventory)
            self.hide_chat()