from data.system_dir.buttons import ExitToMenuBtn
from data.world_dir.load_map_optimiz import generate_level
from data.system_dir.CONST import PLAYERS, BULLETS, DROP_ITEMS,  WIDTH, HEIGHT, MAP_WH, PG


class Detection:
    def __init__(self, screen, GlobalFlags, player, chat):
        """Объекты"""
        self.screen = screen
        self.GF = GlobalFlags
        self.player = player
        self.chat = chat
        """Кнопки"""
        self.exit_btn = ExitToMenuBtn(screen)
        """Флаги"""
        self.chat_detect = False  # чат
        self.minimap_detect = False  # миникарта
        """Переменные"""
        self.Xcords = 0  # координаты карты X
        self.Ycords = 0  # координаты карты Y
        self.map_conv = generate_level()  # мир
        PLAYERS.add(self.player)

    def draw_all(self):
        self.screen.blit(self.map_conv, (self.Xcords, self.Ycords))  # отображаем мир и двигаем его относительно игрока
        DROP_ITEMS.draw(self.screen)
        PLAYERS.draw(self.screen)
        BULLETS.draw(self.screen)
        self.player.draw_all(self.screen)

        if self.player.inv_open:
            if not self.chat_detect:
                self.exit_btn.draw()  # отрисовываем кнопку выхода в меню

        if self.minimap_detect:
            self.minimap.draw(self.screen, self.player)  # получаем координаты и отображаем миникарту

        if self.chat_detect:
            self.chat.draw(self.screen)

    def handle_event(self):
        self.player.moving(PG.key.get_pressed())
        if self.player.inv_open:
            if self.player.taken_item:
                self.player.taken_item.moving()
        for event in PG.event.get():
            if event.type == PG.QUIT:
                self.GF.RUNNING = False
                break

            if event.type == PG.KEYDOWN:
                if event.key == PG.K_RETURN:
                    # детектим откртие чата
                    self.player.can_move = not self.player.can_move
                    self.player.can_action = not self.player.can_action
                    self.chat_detect = not self.chat_detect
                    self.chat.OnOff = self.chat_detect
                    if not self.chat_detect:
                        self.chat.update(self.player)
                if self.chat_detect:
                    self.chat.keyboard_action(event)

                if event.key == PG.K_ESCAPE:  # детектим открытие инвентаря
                    self.player.inv_open = not self.player.inv_open
                self.player.update_keyboard(event.key)
                continue

            if event.type == PG.MOUSEBUTTONDOWN:
                self.player.update_mouse(event.button)
                if self.chat_detect:
                    self.chat.mouse_action(event)
                if self.player.inv_open:
                    # выходим из игры при нажатии кнопки
                    if self.exit_btn.exit_button.collidepoint(PG.mouse.get_pos()) and not self.chat_detect:
                        self.GF.RUNNING = False
                continue

        DROP_ITEMS.update(self.player.move_x, self.player.move_y)
        BULLETS.update(self.player)
        self.Xcords = -self.player.move_x + (WIDTH - MAP_WH) / 2
        self.Ycords = -self.player.move_y + (HEIGHT - MAP_WH) / 2
