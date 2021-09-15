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
        self.inventory_detect = False  # инвентарь
        self.minimap_detect = False  # миникарта
        self.hotBar_detect = True  # хотбар
        """Клавиши"""
        self.key = None
        self.mouse_key = None
        """Переменные"""
        self.Xcords = None  # координаты карты X
        self.Ycords = None  # координаты карты Y
        self.map_conv = generate_level()  # мир
        PLAYERS.add(self.player)

    def update_all(self):
        self.player.update(PG.key.get_pressed())
        DROP_ITEMS.update(self.player.move_x, self.player.move_y)
        BULLETS.update(self.player)
        self.Xcords = -self.player.move_x + (WIDTH - MAP_WH) / 2
        self.Ycords = -self.player.move_y + (HEIGHT - MAP_WH) / 2

        if self.inventory_detect and (self.key or self.mouse_key):
            self.player.update_can_craft()

        if self.key:
            self.detect_keys()
            self.key = None

        if self.mouse_key:
            self.detect_mouse_keys()
            self.mouse_key = None

    def draw_all(self):
        self.screen.blit(self.map_conv, (self.Xcords, self.Ycords))  # отображаем мир и двигаем его относительно игрока
        PLAYERS.draw(self.screen)
        DROP_ITEMS.draw(self.screen)
        BULLETS.draw(self.screen)

        if self.hotBar_detect:
            self.player.draw_hotBar(self.screen)  # отрисовывает горячие слоты

        if self.inventory_detect:
            self.player.draw_inventory(self.screen)  # отрисовываем инвентарь
            self.player.draw_craft(self.screen)  # отрисовываем крафты

            if not self.chat_detect:
                self.exit_btn.draw()  # отрисовываем кнопку выхода в меню

        if self.minimap_detect:
            self.minimap.draw(self.screen, self.player)  # получаем координаты и отображаем миникарту

        if self.chat_detect:
            self.chat.draw(self.screen)

    def detect_keys(self):
        if self.key == PG.K_RETURN:  # детектим откртие чата
            self.player.can_move = not self.player.can_move
            self.chat_detect = not self.chat_detect
            self.chat.OnOff = self.chat_detect

            if not self.chat_detect:
                self.chat.update(self.player)

        if self.key == PG.K_ESCAPE:  # детектим открытие инвентаря
            self.inventory_detect = not self.inventory_detect
            self.hotBar_detect = not self.hotBar_detect

    def detect_mouse_keys(self):
        if self.inventory_detect:
            # выходим из игры при нажатии кнопки
            if self.exit_btn.exit_button.collidepoint(PG.mouse.get_pos()) and not self.chat_detect:
                self.GF.RUNNING = False

            # перекладываем предметы в инвентаре
            self.player.mouse_press_detect(self.mouse_key)

            # передаём вращение колёсика в крафты
            self.player.update_craft_list(self.mouse_key)

        if self.hotBar_detect:  # используем выбранный предмет
            self.player.item_action(self.mouse_key)

    def handle_event(self):
        for event in PG.event.get():
            if event.type == PG.QUIT:
                self.GF.RUNNING = False
                break

            if event.type == PG.KEYDOWN:
                self.key = event.key

                if self.chat_detect:
                    self.chat.keyboard_action(event)

                continue

            if event.type == PG.MOUSEBUTTONDOWN:
                self.mouse_key = event.button

                if self.chat_detect:
                    self.chat.mouse_action(event)

                continue

