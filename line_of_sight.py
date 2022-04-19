# Credit to Adam Milazzo, for http://www.adammil.net/blog/v125_Roguelike_Vision_Algorithms.html
import display


class Slope:

    def __init__(self, x, y):
        self.X = x,
        self.Y = y

    def greater_than(self, x, y):
        return self.Y*x > self.X*y

    def greater_than_or_equal_to(self, x, y):
        return self.Y*x >= self.X*y

    def lesser_than(self, x, y):
        return self.Y*x < self.X*y


def compute(origin, range_limit):
    # make origin visible
    for i in range(8):
        __compute(i, origin, range_limit, 1, Slope(1, 1), Slope(0, 1))


def __compute(octant, origin, range_limit, x, top, bottom):
    pass


def blocks_light(x, y, octant, origin):
    nx = origin(0)
    ny = origin(1)
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
    return not display.check_walls_and_doors(nx, ny)


def set_visible(x, y, octant, origin):
    nx = origin(0)
    ny = origin(1)
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
    __set_visible(nx, ny)


def __set_visible(x, y):
    display.reveal(x, y)
