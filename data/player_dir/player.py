import pygame
from data.system_dir.CONST import WIDTH, HEIGHT
from data.system_dir.item_list import return_item, items_id, inventory_crafting_list


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        """Игрок"""
        self.image = pygame.Surface((25, 25))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (WIDTH / 2 - 12, HEIGHT / 2 - 12)
        self.move_x = 0
        self.move_y = 0
        self.can_move = True
        """Инвентарь"""
        self.inv_image = pygame.image.load('data/textures_dir/interface/inventory.png')
        self.inv_rect = self.inv_image.get_rect()
        self.cell_x = 8  # количество клеток по X
        self.cell_y = 4  # количество клеток по Y
        self.side = 75  # сторона клетки
        self.invW = self.side * self.cell_x
        self.invH = self.side * self.cell_y
        self.invX = WIDTH - self.invW - 20
        self.invY = 20
        self.taken = False
        self.division = False
        self.taken_item = None
        self.inv_cells = [[None for _ in range(self.cell_x)] for _ in range(self.cell_y)]
        self.items_group = pygame.sprite.Group()
        self.inventory_canvas = pygame.Surface((WIDTH, HEIGHT))
        """Хотбар"""
        self.hotBarCell_pos = 0
        self.hotBar_group = pygame.sprite.Group()
        self.hotBar_canvas = pygame.Surface((WIDTH, HEIGHT))
        """Крафты"""
        self.craftingW = 200
        self.craftingH = 245
        self.craftingX = WIDTH - self.craftingW - 20
        self.craftingY = self.invY + self.invH
        self.craft_screen = pygame.Surface((self.craftingW, self.craftingH))
        self.craft_index = 0
        self.can_craft = []
        self.inv_items_count = {}
        self.items_can_craft = pygame.sprite.Group()

    def player_class(self):
        pass

    def update(self, keys):  # обновление всех действий связанных с игроком
        self.moving(keys)
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

    def item_action(self, mouse_key):  # вычисляем положение выбранной ячейки и выполняем с ней действие
        if mouse_key == 5:
            self.hotBarCell_pos -= 1
            if self.hotBarCell_pos < 0:
                self.hotBarCell_pos = self.cell_x - 1

        elif mouse_key == 4:
            self.hotBarCell_pos += 1
            if self.hotBarCell_pos > self.cell_x - 1:
                self.hotBarCell_pos = 0

        elif mouse_key == 1:
            item = self.inv_cells[0][self.hotBarCell_pos]
            if item:
                if item.item_type == 'weapon':
                    item.fire(self.move_x, self.move_y)
    """
    ********************************************************************************************************************
    Инвентарь
    ********************************************************************************************************************
    """
    def draw_inventory(self, screen):  # отрисовываем инвентарь
        # очищаем холст
        self.inventory_canvas.fill((0, 0, 0))
        # делаем холст прозрачным
        self.inventory_canvas.set_colorkey((0, 0, 0))

        pygame.draw.rect(self.inventory_canvas, (255, 0, 0), (self.invX, self.invY, self.invW, self.invH), 1)  # отладка

        # накладываем текстуру инвентаря
        self.inventory_canvas.blit(self.inv_image, (self.invX, self.invY))

        # отрисовываем предмет, который двигаем
        if self.taken:
            self.taken_item.moving()

        # отрисовываем предметы
        self.items_group.draw(self.inventory_canvas)

        # отрисовываем количество предметов
        for y in range(len(self.inv_cells)):
            for x in range(len(self.inv_cells[y])):
                if self.inv_cells[y][x]:
                    if self.inv_cells[y][x].item_type == 'item':
                        cell = self.inv_cells[y][x]
                        stack_style = pygame.font.Font(None, 30)
                        text = stack_style.render(f"{cell.count}", False, (255, 255, 255))
                        self.inventory_canvas.blit(text, (cell.rect.x + 40, cell.rect.y + 40))
        if self.taken_item:
            if self.taken_item.item_type == 'item':
                cell = self.taken_item
                stack_style = pygame.font.Font(None, 30)
                text = stack_style.render(f"{cell.count}", False, (255, 255, 255))
                self.inventory_canvas.blit(text, (cell.rect.x + 40, cell.rect.y + 40))

        # накладываем холст инвентаря на главный холст
        screen.blit(self.inventory_canvas, (0, 0))

    def draw_hotBar(self, screen):
        # очищаем холст
        self.hotBar_canvas.fill((0, 0, 0))

        # делаем его прозрачным
        self.hotBar_canvas.set_colorkey((0, 0, 0))

        # отрисовываем клетки хотбара
        for x in range(self.cell_x):
            pygame.draw.rect(self.hotBar_canvas,
                             (255, 255, 255),
                             (self.invX + self.side * x, self.invY, self.side, self.side), 1)

        # обновляем хотбар
        self.update_hotBar()

        # отрисовываем предметы в хотбаре
        self.hotBar_group.draw(self.hotBar_canvas)

        # отрисовываем количество предметов
        for x in range(len(self.inv_cells[0])):
            if self.inv_cells[0][x]:
                if self.inv_cells[0][x].item_type == 'item':
                    cell = self.inv_cells[0][x]
                    stack_style = pygame.font.Font(None, 30)
                    text = stack_style.render(f"{cell.count}", False, (255, 255, 255))
                    self.hotBar_canvas.blit(text, (cell.rect.x + 40, cell.rect.y + 40))

        # отрисовываем выбраную ячейку
        pygame.draw.rect(self.hotBar_canvas,
                         (0, 0, 255),
                         (self.invX + self.hotBarCell_pos * self.side, self.invY, self.side, self.side), 5)

        # накладываю холст хотбара на главный холст
        screen.blit(self.hotBar_canvas, (0, 0))

    def update_hotBar(self):
        self.hotBar_group.empty()  # очищаем при открытие инвенторя
        for item in self.inv_cells[0]:  # отрисовываем вещи в хотбаре
            if item:
                self.hotBar_group.add(item)

    def mouse_press_detect(self, mouse_key):  # механика перетаскивания вещей в инвентаре
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        selected_cell_x = (mouse_pos_x - self.invX) // self.side
        selected_cell_y = (mouse_pos_y - self.invY) // self.side
        if 0 <= selected_cell_x <= self.cell_x - 1 and 0 <= selected_cell_y <= self.cell_y - 1:
            selected_cell = self.inv_cells[selected_cell_y][selected_cell_x]
            if mouse_key == 1:  # работа с ЛКМ
                if self.taken:
                    if not selected_cell:  # кладём предмет
                        self.taken_item.mobility = False
                        self.taken_item.set_inventory_pos(selected_cell_x, selected_cell_y, self.invX, self.invY)
                        self.inv_cells[selected_cell_y][selected_cell_x] = self.taken_item
                        self.taken_item = None
                        self.taken = False

                    else:
                        if self.taken_item.item_id != selected_cell.item_id:  # меняем предметы местами
                            item = self.taken_item
                            self.taken_item = selected_cell
                            self.inv_cells[selected_cell_y][selected_cell_x] = item
                            self.inv_cells[selected_cell_y][selected_cell_x].mobility = False
                            self.inv_cells[selected_cell_y][selected_cell_x].set_inventory_pos(selected_cell_x,
                                                                                               selected_cell_y,
                                                                                               self.invX, self.invY)
                            self.taken_item.mobility = True
                        else:  # добавляем предметы к предметам
                            taken_item_count = self.taken_item.count
                            item_count = selected_cell.count
                            max_stack = selected_cell.max_count
                            rest = max_stack - item_count
                            if rest != 0:
                                if taken_item_count <= rest:
                                    self.inv_cells[selected_cell_y][selected_cell_x].count += taken_item_count
                                    self.taken_item.kill()
                                    self.taken_item = None
                                    self.taken = False
                                else:
                                    self.inv_cells[selected_cell_y][selected_cell_x].count = max_stack
                                    self.taken_item.count = item_count

                else:
                    if selected_cell:  # берём предмет
                        self.taken = True
                        self.taken_item = selected_cell
                        self.taken_item.mobility = True
                        self.inv_cells[selected_cell_y][selected_cell_x] = None

            if mouse_key == 3:  # работа с ПКМ
                if selected_cell:
                    if self.taken:  # добавляеи по 1 предмету из взятого стака к другому стаку
                        if selected_cell.count < selected_cell.max_count:
                            self.taken_item.count -= 1
                            self.inv_cells[selected_cell_y][selected_cell_x].count += 1
                            if self.taken_item.count == 0:
                                self.taken_item.kill()
                                self.taken_item = None
                                self.taken = False
                    else:
                        if selected_cell.count > 1:  # берём половину предметов
                            self.taken_item = return_item(items_id[selected_cell.item_id])
                            self.items_group.add(self.taken_item)
                            self.taken_item.mobility = True
                            self.taken_item.count = selected_cell.count // 2
                            self.inv_cells[selected_cell_y][selected_cell_x].count -= self.taken_item.count
                            self.taken = True
                else:
                    if self.taken:  # кладём 1 предмет в пустую ячейку
                        self.inv_cells[selected_cell_y][selected_cell_x] = return_item(
                            items_id[self.taken_item.item_id])
                        self.items_group.add(self.inv_cells[selected_cell_y][selected_cell_x])
                        self.inv_cells[selected_cell_y][selected_cell_x].set_inventory_pos(selected_cell_x,
                                                                                           selected_cell_y,
                                                                                           self.invX, self.invY)
                        self.taken_item.count -= 1
                        if self.taken_item.count == 0:
                            self.taken_item.kill()
                            self.taken_item = None
                            self.taken = False

        elif WIDTH - 105 <= mouse_pos_x <= WIDTH - 30 and 405 <= mouse_pos_y <= 480:  # крафт
            spent = False
            if mouse_key == 1:
                if len(self.can_craft) != 0:
                    if self.taken_item:
                        if (self.taken_item.count < self.taken_item.max_count and
                                self.taken_item.item_id == self.can_craft[self.craft_index]):
                            self.taken_item.count += 1
                            spent = True

                    else:
                        self.taken_item = return_item(items_id[self.can_craft[self.craft_index]])
                        self.items_group.add(self.taken_item)
                        self.taken_item.mobility = True
                        self.taken = True
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

    def append_item(self, item):  # механика добавления предмета в инвентарь
        break_flag = False
        for y in range(self.cell_y):
            for x in range(self.cell_x):
                if self.inv_cells[y][x]:
                    if (self.inv_cells[y][x].item_id == item.item_id and
                            self.inv_cells[y][x].count < self.inv_cells[y][x].max_count):
                        self.inv_cells[y][x].count += 1
                        break_flag = True
                        break
                else:
                    item.set_inventory_pos(x, y, self.invX, self.invY)
                    self.items_group.add(item)
                    self.inv_cells[y][x] = item
                    break_flag = True
                    break
            if break_flag:
                break

    def inventory_clear(self):  # Очистка инвентаря
        self.inv_cells = [[None for _ in range(self.cell_x)] for _ in range(self.cell_y)]
        self.items_group.empty()
    """
    ********************************************************************************************************************
    КРАФТЫ
    ********************************************************************************************************************
    """
    def draw_craft(self, screen):
        # очищаем холст
        self.craft_screen.fill((0, 0, 0))

        # делаем холст прозрачным
        self.craft_screen.set_colorkey((0, 0, 0))

        pygame.draw.rect(self.craft_screen, (255, 0, 0), (0, 0, self.craftingW, self.craftingH), 1)  # отладка

        # отрисовываем ячейки крафта
        pygame.draw.rect(self.craft_screen, (255, 255, 255), (120, 10, 65, 65), 5)
        pygame.draw.rect(self.craft_screen, (255, 255, 255), (115, 85, 75, 75), 5)
        pygame.draw.rect(self.craft_screen, (255, 255, 255), (120, 170, 65, 65), 5)

        # отрисовываем 3 предмета из списка возможных крафтов
        self.items_can_craft.draw(self.craft_screen)

        # накладываем холст крафтов на главный холст
        screen.blit(self.craft_screen, (self.craftingX, self.craftingY))

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

    def update_craft_list(self, spin):
        self.items_can_craft.empty()
        if spin == 5:
            self.craft_index += 1
        elif spin == 4:
            self.craft_index -= 1

        if self.craft_index < 0:
            self.craft_index = 0
        elif self.craft_index >= len(self.can_craft):
            self.craft_index = len(self.can_craft) - 1

        if len(self.can_craft) == 0:
            pass
        elif len(self.can_craft) == 1:
            item = return_item(items_id[self.can_craft[self.craft_index]])
            item.set_crafting_pos(115, 85, 1)
            self.items_can_craft.add(item)
        else:
            if self.craft_index == 0:
                item = return_item(items_id[self.can_craft[self.craft_index]])
                item.set_crafting_pos(115, 85, 1)
                self.items_can_craft.add(item)
                item = return_item(items_id[self.can_craft[self.craft_index + 1]])
                item.set_crafting_pos(120, 170, 2)
                self.items_can_craft.add(item)
            elif self.craft_index == len(self.can_craft) - 1:
                item = return_item(items_id[self.can_craft[self.craft_index - 1]])
                item.set_crafting_pos(120, 10, 2)
                self.items_can_craft.add(item)
                item = return_item(items_id[self.can_craft[self.craft_index]])
                item.set_crafting_pos(115, 85, 1)
                self.items_can_craft.add(item)
            else:
                item = return_item(items_id[self.can_craft[self.craft_index - 1]])
                item.set_crafting_pos(120, 10, 2)
                self.items_can_craft.add(item)
                item = return_item(items_id[self.can_craft[self.craft_index]])
                item.set_crafting_pos(115, 85, 1)
                self.items_can_craft.add(item)
                item = return_item(items_id[self.can_craft[self.craft_index + 1]])
                item.set_crafting_pos(120, 170, 2)
                self.items_can_craft.add(item)
