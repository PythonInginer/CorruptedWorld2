from data.system_dir.CONST import WIDTH, HEIGHT, FPS, GlobalFlags, PG
from data.chat_dir.commands import set_player_pos
"""импорт классов"""
from data.chat_dir.chat import Chat
from data.player_dir.playerV2 import Player
from data.system_dir.minimap import Minimap
from data.system_dir.action_detector import Detection


screen = PG.display.set_mode((WIDTH, HEIGHT))
PG.event.set_allowed([PG.QUIT, PG.KEYDOWN, PG.MOUSEBUTTONDOWN])


fpsClock = PG.time.Clock()

player = Player()
minimap = Minimap()
chat = Chat()
GF = GlobalFlags()
detection = Detection(screen, GF, player, chat)

set_player_pos(player, 0, 0)


def game():
    while GF.RUNNING:
        screen.fill((0, 0, 0))  # после этой строки пишем все обновления и отрисовки
        screen.set_colorkey((0, 0, 0))

        detection.handle_event()
        detection.draw_all()

        PG.display.flip()
        fpsClock.tick(FPS)
    PG.quit()


if __name__ == "__main__":
    game()
