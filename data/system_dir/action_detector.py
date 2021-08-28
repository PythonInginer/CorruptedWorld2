import pygame
from data.system_dir.go_to_the_menu import ExitGameBtn


class Detection:
    def __init__(self, screen, GlobalFlags, crafting):
        """Объекты"""
        self.screen = screen
        self.GF = GlobalFlags
        self.crafting = crafting
        """Кнопки"""
        self.exit_btn = ExitGameBtn(screen)
        """Флаги"""
        self.chat_detect = False  # чат
        self.inventory_detect = False  # инвентарь
        self.minimap_detect = False  # миникарта
        self.hotBar_detect = True  # хотбар

    def detect_keys(self, key, chat, player, inventory):
        if key == pygame.K_RETURN:  # детектим откртие чата
            player.can_move = not player.can_move
            self.chat_detect = not self.chat_detect

            chat.open_close_chat(self.chat_detect, player, inventory)

        if key == pygame.K_ESCAPE:  # детектим открытие инвентаря
            self.inventory_detect = not self.inventory_detect
            self.hotBar_detect = not self.hotBar_detect

            self.crafting.update_data(inventory.inventory_cells)

            self.crafting.update_can_craft()
            inventory.update_can_craft(self.crafting.can_craft, self.crafting.craft_list_index)

    def detect_mouse_keys(self, mouse_key, inventory, player):
        if self.inventory_detect:  # обновляем крафты
            self.crafting.update_can_craft()
            inventory.update_can_craft(self.crafting.can_craft, self.crafting.craft_list_index)

        if self.inventory_detect:  # перекладываем предметы в инвентаре
            inventory.mouse_press_detect(mouse_key)

        if self.inventory_detect and not self.chat_detect:  # выходим из игры при нажатии кнопки
            if self.exit_btn.exit_button.collidepoint(pygame.mouse.get_pos()):
                self.GF.RUNNING = False

        if self.hotBar_detect:  # используем выбранный предмет
            inventory.item_action(mouse_key, player)

        if self.inventory_detect:  # передаём вращение колёсика в крафты
            self.crafting.update_craft_list(mouse_key)

    def always_update(self, inventory, minimap, player):
        if self.hotBar_detect:  # отрисовывает горячие слоты
            inventory.draw_hotBar(self.screen)

        if self.inventory_detect:  # отрисовываем крафты
            self.crafting.update_all()

        if self.inventory_detect:  # отрисовываем инвентарь, если была нажата клавиша ESC
            inventory.draw_inventory(self.screen)

        if self.inventory_detect and not self.chat_detect:  # отрисовываем кнопку выхода в меню
            self.exit_btn.draw()

        if self.minimap_detect:  # отрисовываем карту, если в настройках была нажата галочка
            minimap.draw(self.screen, player)  # получаем координаты и отображаем миникарту
