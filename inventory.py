import pygame
from item_list import get_key, items
from CONST import WIDTH, HEIGHT, STACK


class Inventory:
    def __init__(self):
        self.cell_x = 8  # количество клеток по X
        self.cell_y = 4  # количество клеток по Y
        self.side = 75  # сторона клетки
        self.W = self.side * self.cell_x
        self.H = self.side * self.cell_y
        self.X = WIDTH - self.W - 20
        self.Y = 20
        self.taken = False
        self.taken_item = None
        self.division = False
        self.inventory_cells = []
        self.items_group = pygame.sprite.Group()
        self.hot_bar_group = pygame.sprite.Group()
        self.inventory_canvas = pygame.Surface((WIDTH, HEIGHT))
        self.hot_bar_canvas = pygame.Surface((WIDTH, HEIGHT))

    def draw_inventory(self, screen):  # отрисовываем инвентарь

        self.inventory_canvas.fill((0, 0, 0))  # очищаем холст
        self.inventory_canvas.set_colorkey((0, 0, 0))  # делаем холст прозрачным

        self.create_inventory()  # отрисовываем сетку инвентаря
        if self.taken:
            self.taken_item.moving()
        self.items_group.draw(self.inventory_canvas)  # отрисовываем предметы
        self.draw_items_count()  # отрисовываем количество предметов

        screen.blit(self.inventory_canvas, (0, 0))

    def hot_bar(self, screen):
        self.hot_bar_canvas.fill((0, 0, 0))
        self.hot_bar_canvas.set_colorkey((0, 0, 0))

        self.create_hot_bar()

        screen.blit(self.hot_bar_canvas, (0, 0))

    def draw_items_count(self):
        for y in range(len(self.inventory_cells)):
            for x in range(len(self.inventory_cells[y])):
                if self.inventory_cells[y][x]:
                    cell = self.inventory_cells[y][x]
                    stack_style = pygame.font.Font(None, 30)
                    text = stack_style.render(f"{cell.count}", False, (255, 255, 255))
                    self.inventory_canvas.blit(text, (cell.rect.x + 50, cell.rect.y + 40))
        if self.taken_item:
            cell = self.taken_item
            stack_style = pygame.font.Font(None, 30)
            text = stack_style.render(f"{cell.count}", False, (255, 255, 255))
            self.inventory_canvas.blit(text, (cell.rect.x + 50, cell.rect.y + 40))

    def create_inventory(self):  # создаём инвентарь
        cell_pos_y = 0
        for y in range(self.cell_y):
            cell_pos_x = 0
            self.inventory_cells.append([])
            for x in range(self.cell_x):
                self.inventory_cells[y].append(None)
                pygame.draw.rect(self.inventory_canvas,
                                 (255, 255, 255),
                                 (self.X + cell_pos_x, self.Y + cell_pos_y, self.side, self.side), 1)
                cell_pos_x += self.side
            cell_pos_y += self.side
        pygame.draw.rect(self.inventory_canvas, (255, 0, 0), (self.X, self.Y, self.W, self.H), 5)

    def create_hot_bar(self):
        for x in range(self.cell_x):
            pygame.draw.rect(self.hot_bar_canvas,
                             (255, 255, 255),
                             (self.X + self.side * x, self.Y, self.side, self.side), 1)
        
        for item in self.inventory_cells[0]:
            if item:
                self.hot_bar_group.add(item)

    def mouse_press_detect(self, mouse_key):  # механика перетаскивания вещей в инвентаре
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        selected_cell_x = (mouse_pos_x - self.X) // self.side
        selected_cell_y = (mouse_pos_y - self.Y) // self.side
        if 0 <= selected_cell_x <= self.cell_x - 1 and 0 <= selected_cell_y <= self.cell_y - 1:
            selected_cell = self.inventory_cells[selected_cell_y][selected_cell_x]
            if mouse_key == 1:  # работа с ЛКМ
                if self.taken:
                    if not selected_cell:  # кладём предмет
                        self.taken_item.mobility = False
                        self.taken_item.set_pos(selected_cell_x, selected_cell_y, self.X, self.Y)
                        self.inventory_cells[selected_cell_y][selected_cell_x] = self.taken_item
                        self.taken_item = None
                        self.taken = False

                    else:
                        if self.taken_item.id != selected_cell.id:  # меняем предметы местами
                            item = self.taken_item
                            self.taken_item = selected_cell
                            self.inventory_cells[selected_cell_y][selected_cell_x] = item
                            self.inventory_cells[selected_cell_y][selected_cell_x].mobility = False
                            self.inventory_cells[selected_cell_y][selected_cell_x].set_pos(selected_cell_x,
                                                                                           selected_cell_y,
                                                                                           self.X, self.Y)
                            self.taken_item.mobility = True
                        else:  # добавляем предметы к предметам
                            taken_item_count = self.taken_item.count
                            item_count = selected_cell.count
                            rest = STACK - item_count
                            if rest != 0:
                                if taken_item_count <= rest:
                                    self.inventory_cells[selected_cell_y][selected_cell_x].count += taken_item_count
                                    self.taken_item.kill()
                                    self.taken_item = None
                                    self.taken = False
                                else:
                                    self.inventory_cells[selected_cell_y][selected_cell_x].count = STACK
                                    self.taken_item.count = item_count

                else:
                    if selected_cell:  # берём предмет
                        self.taken = True
                        self.taken_item = selected_cell
                        self.taken_item.mobility = True
                        self.inventory_cells[selected_cell_y][selected_cell_x] = None

            if mouse_key == 3:  # работа с ПКМ
                if selected_cell:
                    if self.taken:  # добавляеи по 1 предмету из взятого стака к другому стаку
                        if selected_cell.count < STACK:
                            self.taken_item.count -= 1
                            self.inventory_cells[selected_cell_y][selected_cell_x].count += 1
                            if self.taken_item.count == 0:
                                self.taken_item.kill()
                                self.taken_item = None
                                self.taken = False
                    else:
                        if selected_cell.count > 1:  # берём половину предметов
                            self.taken_item = items(get_key(selected_cell.id))
                            self.items_group.add(self.taken_item)
                            self.taken_item.mobility = True
                            self.taken_item.count = selected_cell.count // 2
                            self.inventory_cells[selected_cell_y][selected_cell_x].count -= self.taken_item.count
                            self.taken = True
                else:
                    if self.taken:  # кладём 1 предмет в пустую ячейку
                        self.inventory_cells[selected_cell_y][selected_cell_x] = items(get_key(self.taken_item.id))
                        self.items_group.add(self.inventory_cells[selected_cell_y][selected_cell_x])
                        self.inventory_cells[selected_cell_y][selected_cell_x].set_pos(selected_cell_x,
                                                                                       selected_cell_y,
                                                                                       self.X, self.Y)
                        self.taken_item.count -= 1
                        if self.taken_item.count == 0:
                            self.taken_item.kill()
                            self.taken_item = None
                            self.taken = False

    def append_item(self, item):  # механика добавления предмета в инвентарь
        break_flag = False
        for y in range(self.cell_y):
            for x in range(self.cell_x):
                if self.inventory_cells[y][x]:
                    if self.inventory_cells[y][x].id == item.id and self.inventory_cells[y][x].count < STACK:
                        self.inventory_cells[y][x].count += 1
                        break_flag = True
                        break
                else:
                    item.set_pos(x, y, self.X, self.Y)
                    self.items_group.add(item)
                    self.inventory_cells[y][x] = item
                    break_flag = True
                    break
            if break_flag:
                break

    def inventory_clear(self):
        self.inventory_cells.clear()
        self.items_group.empty()
