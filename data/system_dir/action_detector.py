import pygame
from data.system_dir.go_to_the_menu import ExitGameBtn
from data.world_dir.load_map_optimiz import generate_level
from data.system_dir.CONST import PLAYERS, BULLETS, WIDTH, HEIGHT, MAP_WH


class Detection:
    def __init__(self, screen, GlobalFlags, player, chat):
        """Объекты"""
        self.screen = screen
        self.GF = GlobalFlags
        self.player = player
        self.chat = chat
        """Кнопки"""
        self.exit_btn = ExitGameBtn(screen)
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

    def update_all(self):
        self.player.update(pygame.key.get_pressed())
        PLAYERS.add(self.player)
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

    def detect_keys(self):
        if self.key == pygame.K_RETURN:  # детектим откртие чата
            self.player.can_move = not self.player.can_move
            self.chat_detect = not self.chat_detect

            self.chat.open_close_chat(self.chat_detect, self.player)

        if self.key == pygame.K_ESCAPE:  # детектим открытие инвентаря
            self.inventory_detect = not self.inventory_detect
            self.hotBar_detect = not self.hotBar_detect

    def detect_mouse_keys(self):
        if self.inventory_detect:
            # выходим из игры при нажатии кнопки
            if self.exit_btn.exit_button.collidepoint(pygame.mouse.get_pos()) and not self.chat_detect:
                self.GF.RUNNING = False

            # перекладываем предметы в инвентаре
            self.player.mouse_press_detect(self.mouse_key)

            # передаём вращение колёсика в крафты
            self.player.update_craft_list(self.mouse_key)

        if self.hotBar_detect:  # используем выбранный предмет
            self.player.item_action(self.mouse_key)

    def get_keys(self, key):
        self.key = key

    def get_mouse_keys(self, mouse_key):
        self.mouse_key = mouse_key
