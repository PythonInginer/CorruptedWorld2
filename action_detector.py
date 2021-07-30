import pygame


class Detection:
    def __init__(self):
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

    def detect_mouse_keys(self, mouse_key, inventory):
        if self.inventory_detect:
            inventory.mouse_press_detect(mouse_key)
        if self.hotBar_detect:
            inventory.item_action(mouse_key)

    def always_update(self, screen, inventory, minimap, player):
        if self.hotBar_detect:  # отрисовывает горячие слоты
            inventory.draw_hotBar(screen)

        if self.inventory_detect:  # отрисовываем инвентарь, если была нажата клавиша ESC
            inventory.draw_inventory(screen)

        if self.minimap_detect:  # отрисовываем карту, если в настройках была нажата галочка
            minimap.draw(screen, player)  # получаем координаты и отображаем миникарту
