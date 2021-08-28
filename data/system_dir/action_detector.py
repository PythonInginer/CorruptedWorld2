import pygame
from data.system_dir.go_to_the_menu import ExitGameBtn
from data.world_dir.load_map_optimiz import generate_level
from data.system_dir.CONST import PLAYERS, BULLETS, WIDTH, HEIGHT, MAP_WH


class Detection:
    def __init__(self, screen, GlobalFlags, player, inventory, crafting, chat):
        """Объекты"""
        self.screen = screen
        self.GF = GlobalFlags
        self.player = player
        self.inventory = inventory
        self.crafting = crafting
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
        PLAYERS.update()
        BULLETS.update(self.player)
        self.Xcords = -self.player.move_x + (WIDTH - MAP_WH) / 2
        self.Ycords = -self.player.move_y + (HEIGHT - MAP_WH) / 2

        if self.inventory_detect and (self.key or self.mouse_key):
            self.crafting.update_can_craft()
            self.inventory.update_can_craft(self.crafting.can_craft, self.crafting.craft_list_index)

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

    def get_keys(self, key):
        self.key = key

    def get_mouse_keys(self, mouse_key):
        self.mouse_key = mouse_key

    def detect_keys(self):
        if self.key == pygame.K_RETURN:  # детектим откртие чата
            self.player.can_move = not self.player.can_move
            self.chat_detect = not self.chat_detect

            self.chat.open_close_chat(self.chat_detect, self.player, self.inventory)

        if self.key == pygame.K_ESCAPE:  # детектим открытие инвентаря
            self.inventory_detect = not self.inventory_detect
            self.hotBar_detect = not self.hotBar_detect

            self.crafting.update_data(self.inventory.inventory_cells)

    def detect_mouse_keys(self):
        if self.inventory_detect:
            # выходим из игры при нажатии кнопки
            if self.exit_btn.exit_button.collidepoint(pygame.mouse.get_pos()) and not self.chat_detect:
                self.GF.RUNNING = False

            # перекладываем предметы в инвентаре
            self.inventory.mouse_press_detect(self.mouse_key)

            # передаём вращение колёсика в крафты
            self.crafting.update_craft_list(self.mouse_key)

        if self.hotBar_detect:  # используем выбранный предмет
            self.inventory.item_action(self.mouse_key, self.player)

    def always_update(self):
        if self.hotBar_detect:
            self.inventory.draw_hotBar(self.screen)  # отрисовывает горячие слоты

        if self.inventory_detect:
            self.crafting.draw_craft()  # отрисовываем крафты

            self.inventory.draw_inventory(self.screen)  # отрисовываем инвентарь, если была нажата клавиша ESC

            if not self.chat_detect:
                self.exit_btn.draw()  # отрисовываем кнопку выхода в меню

        if self.minimap_detect:
            self.minimap.draw(self.screen, self.player)  # получаем координаты и отображаем миникарту
