import pygame
from data.system_dir.CONST import WIDTH, HEIGHT, DROP_ITEMS, CELL_X, CELL_Y, CELL_WH
from data.system_dir.item_list import return_item, items_id, inventory_crafting_list


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        """Система"""
        self.taken_item_group = pygame.sprite.Group()
        self.inv_open = False  # открыт инвентарь
        self.can_move = True  # может ли двигаться
        self.can_action = True  # может ли взаимодействовать с предметами

        """Игрок"""
        self.image = pygame.Surface((25, 25))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (WIDTH / 2 - self.image.get_width() // 2, HEIGHT / 2 - self.image.get_height() // 2)
        self.move_x = 0
        self.move_y = 0

        """Общие параметры"""
        self.cell_image = pygame.image.load('data/textures_dir/interface/standart_cell.png')
        self.chosen_cell_image = pygame.image.load('data/textures_dir/interface/chousen_cell.png')
        self.inventory_canvas = pygame.Surface((WIDTH, HEIGHT))
        self.general_shiftX = WIDTH - 20

        """Инвентарь"""
        self.inv_image = pygame.image.load('data/textures_dir/interface/inventory.png')
        self.invW = CELL_WH * CELL_X
        self.invH = CELL_WH * CELL_Y
        self.invX = self.general_shiftX - self.invW
        self.invY = 20
        self.division = False
        self.taken_item = None
        self.inv_cells = [[None for _ in range(CELL_X)] for _ in range(CELL_Y)]
        self.inv_cells_group = pygame.sprite.Group()

        self.inv_rect = pygame.Rect(self.invX, self.invY, self.invW, self.invH)

        """Хотбар"""
        self.hotBar_image = pygame.image.load('data/textures_dir/interface/hotbar.png')

        self.hotBar_chosen_cell = 0
        self.hotBar_group = pygame.sprite.Group()

        """Крафты"""
        self.craftingW = 200
        self.craftingH = 212
        self.craftingX = self.general_shiftX - self.craftingW
        self.craftingY = self.invY + self.invH
        self.chose_craft = 0
        self.can_craft = []
        self.inv_items_count = {}
        self.items_can_craft = pygame.sprite.Group()

        self.craft_rect = pygame.Rect(self.craftingX - CELL_WH + self.craftingW,
                                      self.craftingY + 74,
                                      CELL_WH, CELL_WH)

    def player_class(self):
        pass

    """
    ********************************************************************************************************************
    Обновление/отрисовка
    ********************************************************************************************************************
    """
    def update_keyboard(self, key):
        if self.can_action:
            self.objects_motions(key)

    def update_mouse(self, button):
        if self.inv_open:
            self.spin_craft_list(button)
            self.mouse_press_detect(button)
            # обновляем координаты предмета, который двигаем
            if self.taken_item:
                self.taken_item.moving()
        else:
            if self.can_action:
                self.item_action(button)

    def draw_all(self, screen):
        # очищаем холст
        # делаем холст прозрачным
        self.inventory_canvas.fill((0, 0, 0))
        self.inventory_canvas.set_colorkey((0, 0, 0))

        if self.inv_open:
            self.draw_inventory()
            self.draw_craft()
        else:
            self.draw_hotBar()

        self.taken_item_group.draw(self.inventory_canvas)

        # отрисовываем всё а главном экране
        screen.blit(self.inventory_canvas, (0, 0))

    """
    ********************************************************************************************************************
    Действия игрока
    ********************************************************************************************************************
    """

    def moving(self, keys):  # движение
        if self.can_move:
            if keys[pygame.K_w]:
                self.move_y -= 5

            if keys[pygame.K_s]:
                self.move_y += 5

            if keys[pygame.K_a]:
                self.move_x -= 5

            if keys[pygame.K_d]:
                self.move_x += 5

    def objects_motions(self, key):
        if self.can_action:
            #  поднимаем предметы
            if key == pygame.K_e:
                drop = pygame.sprite.spritecollideany(self, DROP_ITEMS)
                if drop:
                    DROP_ITEMS.remove(drop)
                    drop.drop = False
                    self.append_item(drop)

    def item_action(self, mouse_key):  # вычисляем положение выбранной ячейки и выполняем с ней действие
        if mouse_key == 5:  # колёсико назад
            self.hotBar_chosen_cell -= 1
            if self.hotBar_chosen_cell < 0:
                self.hotBar_chosen_cell = CELL_X - 1

        elif mouse_key == 4:  # колёсико вперёд
            self.hotBar_chosen_cell += 1
            if self.hotBar_chosen_cell > CELL_X - 1:
                self.hotBar_chosen_cell = 0

        elif mouse_key == 1:  # лкм
            item = self.inv_cells[0][self.hotBar_chosen_cell]
            if item:
                if item.item_type == 'weapon':
                    item.fire(self.move_x, self.move_y)

    """
    ********************************************************************************************************************
    Хотбар
    ********************************************************************************************************************
    """

    def draw_hotBar(self):
        # отрисовываем клетки хотбара
        self.inventory_canvas.blit(self.hotBar_image,
                                   (self.invX, self.invY))
        # отрисовываем выбраную ячейку
        self.inventory_canvas.blit(self.chosen_cell_image,
                                   (self.invX + self.hotBar_chosen_cell * CELL_WH, self.invY))
        # обновляем хотбар
        self.update_hotBar()
        # отрисовываем предметы в хотбаре
        self.hotBar_group.draw(self.inventory_canvas)

    def update_hotBar(self):
        self.hotBar_group.empty()  # очищаем при открытие инвенторя
        for item in self.inv_cells[0]:  # отрисовываем вещи в хотбаре
            if item:
                self.hotBar_group.add(item)

    """
    ********************************************************************************************************************
    Инвентарь
    ********************************************************************************************************************
    """

    def draw_inventory(self):  # отрисовываем инвентарь
        pygame.draw.rect(self.inventory_canvas, (255, 0, 0), (self.invX, self.invY, self.invW, self.invH), 1)  # отладка

        # накладываем текстуру инвентаря
        self.inventory_canvas.blit(self.inv_image, (self.invX, self.invY))
        # отрисовываем предметы
        self.inv_cells_group.draw(self.inventory_canvas)
        # накладываем холст инвентаря на главный холст

    def mouse_press_detect(self, mouse_key):  # механика перетаскивания вещей в инвентаре
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        select_cellX = (mouse_pos_x - self.invX) // CELL_WH
        select_cellY = (mouse_pos_y - self.invY) // CELL_WH
        if mouse_key:
            if self.inv_rect.collidepoint(mouse_pos_x, mouse_pos_y):
                selected_cell = self.inv_cells[select_cellY][select_cellX]
                # работа с ЛКМ
                if mouse_key == 1:
                    if self.taken_item:
                        # кладём предмет
                        if not selected_cell:
                            self.taken_item.mobility = False
                            self.taken_item.set_inventory_pos(select_cellX, select_cellY, self.invX, self.invY)
                            self.inv_cells[select_cellY][select_cellX] = self.taken_item
                            self.taken_item_group.remove(self.taken_item)
                            self.inv_cells_group.add(self.taken_item)
                            self.taken_item = None

                        else:
                            # меняем предметы местами
                            if self.taken_item.item_id != selected_cell.item_id:
                                selected_cell.mobility = True
                                self.taken_item.mobility = False
                                self.taken_item_group.remove(self.taken_item)
                                self.taken_item_group.add(selected_cell)
                                self.inv_cells_group.remove(selected_cell)
                                self.inv_cells_group.add(self.taken_item)
                                self.taken_item.set_inventory_pos(select_cellX, select_cellY, self.invX, self.invY)
                                self.inv_cells[select_cellY][select_cellX] = self.taken_item
                                self.taken_item = selected_cell
                            else:
                                # добавляем предметы к предметам
                                rest = selected_cell.max_count - selected_cell.count
                                if rest != 0:
                                    if self.taken_item.count <= rest:
                                        self.inv_cells[select_cellY][select_cellX].count += self.taken_item.count
                                        self.taken_item_group.remove(self.taken_item)
                                        self.taken_item.kill()
                                        self.taken_item = None
                                    else:
                                        self.inv_cells[select_cellY][select_cellX].count = max_stack
                                        self.taken_item.count = item_count

                    else:
                        if selected_cell:  # берём предмет
                            self.inv_cells[select_cellY][select_cellX] = None
                            self.inv_cells_group.remove(selected_cell)
                            self.taken_item = selected_cell
                            self.taken_item.mobility = True
                            self.taken_item_group.add(self.taken_item)

                elif mouse_key == 3:  # работа с ПКМ
                    if selected_cell:
                        if self.taken_item:  # добавляеи по 1 предмету из взятого стака к другому стаку
                            if selected_cell.count < selected_cell.max_count:
                                self.taken_item.count -= 1
                                self.inv_cells[select_cellY][select_cellX].count += 1
                                if self.taken_item.count == 0:
                                    self.taken_item_group.remove(self.taken_item)
                                    self.taken_item.kill()
                                    self.taken_item = None
                        else:
                            if selected_cell.count > 1:  # берём половину предметов
                                self.taken_item = return_item(items_id[selected_cell.item_id])
                                self.taken_item.count = selected_cell.count // 2
                                self.taken_item_group.add(self.taken_item)
                                self.taken_item.mobility = True
                                self.inv_cells[select_cellY][select_cellX].count -= self.taken_item.count
                    else:
                        if self.taken_item:  # кладём 1 предмет в пустую ячейку
                            self.inv_cells[select_cellY][select_cellX] = return_item(items_id[self.taken_item.item_id])
                            self.inv_cells_group.add(self.inv_cells[select_cellY][select_cellX])
                            self.inv_cells[select_cellY][select_cellX].set_inventory_pos(select_cellX,
                                                                                         select_cellY,
                                                                                         self.invX, self.invY)
                            self.taken_item.count -= 1
                            if self.taken_item.count == 0:
                                self.taken_item_group.remove(self.taken_item)
                                self.taken_item.kill()
                                self.taken_item = None

            elif self.craft_rect.collidepoint(mouse_pos_x, mouse_pos_y):  # крафт
                spent = False
                if mouse_key == 1:
                    if len(self.can_craft) != 0:
                        if self.taken_item:
                            if (self.taken_item.count < self.taken_item.max_count and
                                    self.taken_item.item_id == self.can_craft[self.chose_craft]):
                                self.taken_item.count += 1
                                spent = True

                        else:
                            self.taken_item = return_item(items_id[self.can_craft[self.chose_craft]])
                            self.taken_item_group.add(self.taken_item)
                            self.taken_item.mobility = True
                            spent = True

                    if spent:
                        for ic in inventory_crafting_list[self.taken_item.item_id]:
                            index, count = ic
                            flag = False
                            for y in range(len(self.inv_cells)):
                                for x in range(len(self.inv_cells[y])):
                                    if self.inv_cells[y][x]:
                                        if self.inv_cells[y][x].item_id == index:
                                            if self.inv_cells[y][x].count <= count:
                                                count -= self.inv_cells[y][x].count
                                                self.inv_cells[y][x].kill()
                                                self.inv_cells[y][x] = None
                                            else:
                                                self.inv_cells[y][x].count -= count
                                                count = 0
                                            if count == 0:
                                                flag = True
                                                break
                                if flag:
                                    break
            else:
                #  бросаем предмет
                if self.taken_item:
                    self.taken_item.set_drop_pos(self.move_x, self.move_y, self.rect.w, self.rect.h)
                    self.taken_item_group.remove(self.taken_item)
                    self.taken_item.mobility = False
                    self.taken_item.drop = True
                    self.update_items_count()

                    DROP_ITEMS.add(self.taken_item)

                    self.taken_item = None

        self.update_items_count()

    def append_item(self, item):  # механика добавления предмета в инвентарь
        break_flag = False
        for y in range(CELL_Y):
            for x in range(CELL_X):
                if self.inv_cells[y][x]:
                    if self.inv_cells[y][x].stacking:
                        if self.inv_cells[y][x].item_id == item.item_id:
                            rest = self.inv_cells[y][x].max_count - self.inv_cells[y][x].count
                            if rest != 0:
                                if item.count <= rest:
                                    self.inv_cells[y][x].count += item.count
                                    item.kill()
                                    break_flag = True
                                    break
                                else:
                                    self.inv_cells[y][x].count = self.inv_cells[y][x].max_count
                                    item.count -= rest

                else:
                    item.set_inventory_pos(x, y, self.invX, self.invY)
                    self.inv_cells_group.add(item)
                    self.inv_cells[y][x] = item
                    break_flag = True
                    break
            if break_flag:
                break

        self.update_items_count()
        self.update_can_craft()
        self.update_craft_list()

    def inventory_clear(self):  # Очистка инвентаря
        self.inv_cells = [[None for _ in range(self.CELL_X)] for _ in range(self.CELL_Y)]
        self.inv_cells_group.empty()

    def update_items_count(self):
        for y in range(len(self.inv_cells)):
            for x in range(len(self.inv_cells[y])):
                if self.inv_cells[y][x]:
                    self.inv_cells[y][x].count_updater()

        if self.taken_item:
            self.taken_item.count_updater()

    """
    ********************************************************************************************************************
    КРАФТЫ
    ********************************************************************************************************************
    """

    def draw_craft(self):
        pygame.draw.rect(self.inventory_canvas, (255, 0, 0), (self.craftingX, self.craftingY,
                                                              self.craftingW, self.craftingH), 1)  # отладка

        # отрисовываем ячейки крафта
        self.inventory_canvas.blit(self.cell_image,
                                   (self.craftingX - CELL_WH + self.craftingW, self.craftingY + 10))
        self.inventory_canvas.blit(self.chosen_cell_image,
                                   (self.craftingX - CELL_WH + self.craftingW, self.craftingY + 74))
        self.inventory_canvas.blit(self.cell_image,
                                   (self.craftingX - CELL_WH + self.craftingW, self.craftingY + 138))

        # отрисовываем 3 предмета из списка возможных крафтов
        self.items_can_craft.draw(self.inventory_canvas)

    def update_can_craft(self):
        self.can_craft = []
        self.inv_items_count = {}
        for y in range(len(self.inv_cells)):
            for x in range(len(self.inv_cells[y])):
                if self.inv_cells[y][x]:
                    if self.inv_cells[y][x].item_id in self.inv_items_count:
                        self.inv_items_count[self.inv_cells[y][x].item_id] += self.inv_cells[y][x].count
                    else:
                        self.inv_items_count[self.inv_cells[y][x].item_id] = self.inv_cells[y][x].count

        for key in inventory_crafting_list.keys():
            can_craft_flag = True
            for index, count in inventory_crafting_list[key]:
                if index not in self.inv_items_count.keys():
                    can_craft_flag = False
                    break
                else:
                    if count > self.inv_items_count[index]:
                        can_craft_flag = False
                        break
            if can_craft_flag:
                self.can_craft.append(key)

    def spin_craft_list(self, spin):
        if spin == 5:
            self.chose_craft += 1
        elif spin == 4:
            self.chose_craft -= 1

        if self.chose_craft < 0:
            self.chose_craft = 0
        elif self.chose_craft >= len(self.can_craft):
            self.chose_craft = len(self.can_craft) - 1

        self.update_craft_list()

    def update_craft_list(self):
        self.items_can_craft.empty()
        if len(self.can_craft) == 0:
            pass
        elif len(self.can_craft) == 1:
            item = return_item(items_id[self.can_craft[self.chose_craft]])
            item.set_crafting_pos(self.craftingX + 115, self.craftingY + 85, 1)
            self.items_can_craft.add(item)
        else:
            if self.chose_craft == 0:
                item = return_item(items_id[self.can_craft[self.chose_craft]])
                item.set_crafting_pos(self.craftingX - CELL_WH + self.craftingW, self.craftingY + 74, 1)
                self.items_can_craft.add(item)
                item = return_item(items_id[self.can_craft[self.chose_craft + 1]])
                item.set_crafting_pos(self.craftingX - CELL_WH + self.craftingW, self.craftingY + 138, 2)
                self.items_can_craft.add(item)
            elif self.chose_craft == len(self.can_craft) - 1:
                item = return_item(items_id[self.can_craft[self.chose_craft - 1]])
                item.set_crafting_pos(self.craftingX - CELL_WH + self.craftingW, self.craftingY + 10, 2)
                self.items_can_craft.add(item)
                item = return_item(items_id[self.can_craft[self.chose_craft]])
                item.set_crafting_pos(self.craftingX - CELL_WH + self.craftingW, self.craftingY + 74, 1)
                self.items_can_craft.add(item)
            else:
                item = return_item(items_id[self.can_craft[self.chose_craft - 1]])
                item.set_crafting_pos(self.craftingX - CELL_WH + self.craftingW, self.craftingY + 10, 2)
                self.items_can_craft.add(item)
                item = return_item(items_id[self.can_craft[self.chose_craft]])
                item.set_crafting_pos(self.craftingX - CELL_WH + self.craftingW, self.craftingY + 74, 1)
                self.items_can_craft.add(item)
                item = return_item(items_id[self.can_craft[self.chose_craft + 1]])
                item.set_crafting_pos(self.craftingX - CELL_WH + self.craftingW, self.craftingY + 138, 2)
                self.items_can_craft.add(item)
