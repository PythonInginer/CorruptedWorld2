from data.chat_dir.commands import set_player_pos, give_item, inventory_clear
from data.system_dir.CONST import WIDTH, HEIGHT
from data.system_dir.CONST import PG
from data.system_dir.input_box import InputBox


class Chat(InputBox):
    def __init__(self,
                 x=WIDTH - 500 - 10,
                 y=HEIGHT - 30 - 20,
                 w=500,
                 h=30,
                 txt_height=20,
                 txt_color=(255, 255, 255),
                 bg_color=(30, 30, 30),
                 outline_color_T=(121, 162, 185,),
                 outline_color_F=(29, 41, 81),
                 msim=100,
                 text=''):
        super().__init__(x, y, w, h, txt_height, txt_color, bg_color, outline_color_T, outline_color_F, msim, text)

    def update(self, player):

        if self.text != '':
            if self.text[0] == '/':
                self.text = self.text.split()
                if self.text[0][1:] == 'tp':
                    set_player_pos(player, int(self.text[1]), int(self.text[2]))
                if self.text[0][1:] == 'give':
                    item_type, item_name = self.text[1].split(':')
                    give_item(player, item_name, int(self.text[2]))
                if self.text[0][1:] == 'inventory':
                    if self.text[1] == 'clear':
                        inventory_clear(player)
            else:
                pass
        self.text = ''
