import display


def move_check(x, y):
    return display.check_walls_and_doors(x, y) and display.check_for_creatures(x, y)


class Creature:

    def __init__(self, floor_plan, x_position, y_position, window, character):
        self.floor_plan = floor_plan
        self.x_position = x_position
        self.y_position = y_position
        self.window = window
        self.character = character

    def move(self, x_pos, y_pos):
        self.x_position = x_pos
        self.y_position = y_pos

    def move_north(self):
        new_x = self.x_position
        new_y = self.y_position - 1
        if move_check(new_x, new_y):
            self.move(new_x, new_y)

    def move_south(self):
        new_x = self.x_position
        new_y = self.y_position + 1
        if move_check(new_x, new_y):
            self.move(new_x, new_y)

    def move_east(self):
        new_x = self.x_position + 1
        new_y = self.y_position
        if move_check(new_x, new_y):
            self.move(new_x, new_y)

    def move_west(self):
        new_x = self.x_position - 1
        new_y = self.y_position
        if move_check(new_x, new_y):
            self.move(new_x, new_y)

    def move_north_west(self):
        new_x = self.x_position - 1
        new_y = self.y_position - 1
        if move_check(new_x, new_y):
            self.move(new_x, new_y)

    def move_south_west(self):
        new_x = self.x_position - 1
        new_y = self.y_position + 1
        if move_check(new_x, new_y):
            self.move(new_x, new_y)

    def move_south_east(self):
        new_x = self.x_position + 1
        new_y = self.y_position + 1
        if move_check(new_x, new_y):
            self.move(new_x, new_y)

    def move_north_east(self):
        new_x = self.x_position + 1
        new_y = self.y_position - 1
        if move_check(new_x, new_y):
            self.move(new_x, new_y)

    def draw_self(self):
        self.window.addch(self.y_position, self.x_position, self.character)
