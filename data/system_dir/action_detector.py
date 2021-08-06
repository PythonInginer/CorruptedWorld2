import pygame
from data.system_dir.go_to_the_menu import ExitGameBtn


class Detection:
    def __init__(self, screen, GlobalFlags):
        """Объекты"""
        self.screen = screen
        """Кнопки"""
        self.exit_btn = ExitGameBtn(screen)
        self.GF = GlobalFlags
        """Флаги"""
        self.chat_detect = False
        self.inventory_detect = False
        self.minimap_detect = True
        self.hotBar_detect = True

    def detect_keys(self, key, chat, player, inventory):
        if key == pygame.K_RETURN:  # детектим откртие чата
            player.can_move = not player.can_move
            self.chat_detect = not self.chat_detect

            chat.open_close_chat(self.chat_detect, player, inventory)

        if key == pygame.K_ESCAPE:  # детектим открытие инвентаря
            self.inventory_detect = not self.inventory_detect
            self.hotBar_detect = not self.hotBar_detect

    def detect_mouse_keys(self, mouse_key, inventory, player):
        if self.inventory_detect:
            inventory.mouse_press_detect(mouse_key)
        if self.inventory_detect:
            if self.exit_btn.exit_button.collidepoint(pygame.mouse.get_pos()):
                self.GF.RUNNING = False
        if self.hotBar_detect:
            inventory.item_action(mouse_key, player)

    def always_update(self, inventory, minimap, player):
        if self.hotBar_detect:  # отрисовывает горячие слоты
            inventory.draw_hotBar(self.screen)

        if self.inventory_detect:  # отрисовываем инвентарь, если была нажата клавиша ESC
            inventory.draw_inventory(self.screen)

        if self.inventory_detect:
            self.exit_btn.draw()

        if self.minimap_detect:  # отрисовываем карту, если в настройках была нажата галочка
            minimap.draw(self.screen, player)  # получаем координаты и отображаем миникарту
