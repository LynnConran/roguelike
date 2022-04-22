# Credit to Adam Milazzo, for http://www.adammil.net/blog/v125_Roguelike_Vision_Algorithms.html
import display
import math


class Slope:

    def __init__(self, y, x):
        self.X = x
        self.Y = y

    def greater_than(self, y, x):
        return self.Y * x > self.X * y

    def greater_than_or_equal_to(self, y, x):
        return self.Y * x >= self.X * y

    def less_than(self, y, x):
        return self.Y * x < self.X * y


def get_distance(x, y):
    return math.dist((x, y), (0, 0))


def compute(origin, range_limit, floor_plan, hidden_map, is_player=False):
    if is_player:
        hidden_map = __set_visible(origin[0], origin[1], hidden_map)
    for i in range(8):
        hidden_map = __compute(i, origin, range_limit, 1, Slope(1, 1), Slope(0, 1), floor_plan, hidden_map, is_player)
    return hidden_map


# I barely understand the algorithm at time of writing, it is beyond my capabilities to explain it at the moment.
# In my understanding, it functions similarly to shadowcasting with diamond walls, but with beveled walls instead.
# Please read the website written at the top
def __compute(octant, origin, range_limit, x, top, bottom, floor_plan, hidden_map, is_player):
    while x <= range_limit:
        if top.X == 1:
            top_y = x
        else:
            top_y = (((x * 2 + 1) * top.Y) + top.X) / (top.X * 2)
            if blocks_light(x, top_y, octant, origin, floor_plan):
                if top.greater_than_or_equal_to(top_y * 2 + 1, x * 2) \
                        and not blocks_light(x, top_y + 1, octant, origin, floor_plan):
                    top_y += 1
            else:
                ax = x * 2
                if blocks_light(x + 1, top_y + 1, octant, origin, floor_plan):
                    ax += 1
                if top.greater_than(top_y * 2 + 1, ax):
                    top_y += 1

        if bottom.Y == 0:
            bottom_y = 0
        else:
            bottom_y = (((x * 2 - 1) * bottom.Y) + bottom.X) / (bottom.X * 2)
            if bottom.greater_than_or_equal_to(bottom_y * 2 + 1, x * 2) \
                    and blocks_light(x, bottom_y, octant, origin, floor_plan) \
                    and not blocks_light(x, bottom_y + 1, octant, origin, floor_plan):
                bottom_y += 1

        was_opaque = -1
        y = top_y
        while int(y) >= int(bottom_y):
            if range_limit < 0 or get_distance(x, y) <= range_limit:
                is_opaque = blocks_light(x, y, octant, origin, floor_plan)
                # is_visible = is_opaque or ((y != top_y or top.greater_than(y*4 - 1, x * 4 + 1)) and (y != bottom_y
                #                                                                or bottom.less_than(y*4 + 1, x*4 - 1)))
                is_visible = (is_opaque and was_opaque >= 0) or ((y != top_y or top.greater_than(y * 4 - 1, x * 4 + 1))
                                                                 and (y != bottom_y or bottom.less_than(y * 4 + 1,
                                                                                                        x * 4 - 1)))
                # is_visible deviates from the base code
                if is_visible:
                    hidden_map = set_visible(x, y, octant, origin, hidden_map)  # Change here to let monsters look

                if x != range_limit:
                    if is_opaque:
                        if was_opaque == 0:
                            nx = x * 2
                            ny = y * 2 + 1
                            if blocks_light(x, y + 1, octant, origin, floor_plan):
                                nx -= 1
                            if top.greater_than(ny, nx):
                                if y == bottom_y:
                                    bottom = Slope(ny, nx)
                                    break
                                else:
                                    hidden_map = __compute(octant, origin, range_limit, x + 1, top, Slope(ny, nx),
                                                           floor_plan, hidden_map, is_player)
                            else:
                                if y == bottom_y:
                                    return hidden_map
                        was_opaque = 1
                    else:
                        if was_opaque > 0:
                            nx = x * 2
                            ny = y * 2 + 1
                            if blocks_light(x + 1, y + 1, octant, origin, floor_plan):
                                nx += 1
                            if bottom.greater_than_or_equal_to(ny, nx):
                                return hidden_map
                            top = Slope(ny, nx)
                        was_opaque = 0
            y -= 1
        if was_opaque != 0:
            break
        x += 1
    return hidden_map


def blocks_light(x, y, octant, origin, floor_plan):
    nx = origin[0]
    ny = origin[1]
    if octant == 0:
        nx += x
        ny -= y
    elif octant == 1:
        nx += y
        ny -= x
    elif octant == 2:
        nx -= y
        ny -= x
    elif octant == 3:
        nx -= x
        ny -= y
    elif octant == 4:
        nx -= x
        ny += y
    elif octant == 5:
        nx -= y
        ny += x
    elif octant == 6:
        nx += y
        ny += x
    elif octant == 7:
        nx += x
        ny += y
    return not display.check_walls_and_doors(int(nx), int(ny), floor_plan)


def set_visible(x, y, octant, origin, hidden_map):
    nx = origin[0]
    ny = origin[1]
    if octant == 0:
        nx += x
        ny -= y
    elif octant == 1:
        nx += y
        ny -= x
    elif octant == 2:
        nx -= y
        ny -= x
    elif octant == 3:
        nx -= x
        ny -= y
    elif octant == 4:
        nx -= x
        ny += y
    elif octant == 5:
        nx -= y
        ny += x
    elif octant == 6:
        nx += y
        ny += x
    elif octant == 7:
        nx += x
        ny += y
    return __set_visible(int(nx), int(ny), hidden_map)


def __set_visible(x, y, hidden_map):
    if x < 0 or x >= display.MAIN_WINDOW_SIZE_X or y < 0 or y >= display.MAIN_WINDOW_SIZE_Y:
        return hidden_map
    hidden_map[y][x] = True
    return hidden_map
