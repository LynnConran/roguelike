# Pathfinding algorithm, simple implementation of A*
import math
import global_variables


def search(floor_plan, entity_list, player_position, start, end):
    return __make_path(__a_star_search(MyGraph(floor_plan, entity_list, player_position), start, end))


def __make_path(cell):
    if cell == "Not Found":
        return cell
    movement_list = []
    while cell.parent is not None:
        movement_list.insert(0, cell.position)
        cell = cell.parent
    return movement_list


class MyGraph:

    def __init__(self, floor_plan, entity_list, player_position):
        self.floor_plan = floor_plan
        self.entity_list = entity_list
        self.player_position = player_position

    def __check_walls_and_doors(self, x, y):  # Returns True if valid
        return not (x < 0 or x >= global_variables.MAIN_WINDOW_SIZE_X or y < 0
                    or y >= global_variables.MAIN_WINDOW_SIZE_Y or self.floor_plan[y][x] == '#')

    # def __check_for_critters(self, x, y):
    #     position = (x, y)
    #     for i in self.entity_list:
    #         if position == i.get_x_and_y():
    #             return True
    #     if position == self.player_position:
    #         return True
    #     return False

    def check_valid(self, x, y):
        return self.__check_walls_and_doors(x, y)
               # and not self.__check_for_critters(x, y)


class Cell:

    def __init__(self, parent, position, h):
        self.parent = parent
        self.position = position
        if parent is not None:
            self.g = math.dist(self.parent.position, self.position) + self.parent.g
        else:
            self.g = 0
        self.h = h
        self.f = self.g + self.h


def __heuristic(a, b):
    x1, y1 = a
    x2, y2 = b
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    # h = D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
    return (dx + dy) + ((math.dist((0, 0), (1, 1)) - 2) * min(dx, dy))


def __find_minimum_cost(cell_list):
    minimum = cell_list[0].f
    min_cell = cell_list[0]
    for i in cell_list:
        if i.f < minimum:
            minimum = i.f
            min_cell = i
    return min_cell


def __find_same_position(cell_list, position):
    for i in cell_list:
        if i.position == position:
            return i
    return "None"


def __a_star_search(graph: MyGraph, start, end):
    open = []
    closed = []
    open.append(Cell(None, start, __heuristic(start, end)))
    while len(open) >= 1:
        our_cell = __find_minimum_cost(open)
        open.remove(our_cell)

        for y in range(our_cell.position[1] - 1, our_cell.position[1] + 2):
            for x in range(our_cell.position[0] - 1, our_cell.position[0] + 2):
                if (x, y) == our_cell.position:
                    continue
                if graph.check_valid(x, y):
                    temp = Cell(our_cell, (x, y), __heuristic((x, y), end))
                    if (x, y) == end:
                        return temp
                    other_cell = __find_same_position(open, temp.position)
                    if other_cell != "None":
                        if other_cell.f <= temp.f:
                            continue
                    other_cell = __find_same_position(closed, temp.position)
                    if other_cell != "None":
                        if other_cell.f < temp.f:
                            continue
                    open.append(temp)

        closed.append(our_cell)

    return "Not Found"
