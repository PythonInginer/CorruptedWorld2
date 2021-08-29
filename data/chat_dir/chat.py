import pygame_gui
from data.chat_dir.commands import set_player_pos, give_item, inventory_clear
from data.system_dir.CONST import WIDTH, HEIGHT


class Chat:
    def __init__(self, manager, pg):
        W = 500
        H = 40
        self.pg = pg
        self.manager = manager
        self.chat = pygame_gui.elements.UITextEntryLine(
            relative_rect=self.pg.Rect((WIDTH - W - 20, HEIGHT - H - 10), (W, H)),
            manager=self.manager
        )
        self.hide_chat()

    def show_chat(self):
        self.chat.show()

    def hide_chat(self):
        self.chat.set_text('')
        self.chat.hide()

    def update(self, player):
        text = self.chat.get_text()
        if text != '':
            if text[0] == '/':
                text = text.split()
                if text[0][1:] == 'tp':
                    set_player_pos(player, int(text[1]), int(text[2]))
                if text[0][1:] == 'give':
                    item_type, item_name = text[1].split(':')
                    give_item(player, item_name, int(text[2]))
                if text[0][1:] == 'inventory':
                    if text[1] == 'clear':
                        inventory_clear(player)
            else:
                pass

    def open_close_chat(self, chat_detect, player):
        if chat_detect:
            self.show_chat()
        else:
            self.update(player)
            self.hide_chat()
