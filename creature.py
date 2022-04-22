import display
import line_of_sight


class Creature:

    BASE_LINE_OF_SIGHT = 4

    def __init__(self, x_position, y_position, floor_plan, window, character, color_pair=0):
        self.x_position = x_position
        self.y_position = y_position
        self.floor_plan = floor_plan
        self.window = window
        self.character = character
        self.color_pair = color_pair

    def move(self, x_pos, y_pos):
        self.x_position = x_pos
        self.y_position = y_pos

    def move_north(self):
        new_x = self.x_position
        new_y = self.y_position - 1
        if self.move_check(new_x, new_y):
            self.move(new_x, new_y)

    def move_south(self):
        new_x = self.x_position
        new_y = self.y_position + 1
        if self.move_check(new_x, new_y):
            self.move(new_x, new_y)

    def move_east(self):
        new_x = self.x_position + 1
        new_y = self.y_position
        if self.move_check(new_x, new_y):
            self.move(new_x, new_y)

    def move_west(self):
        new_x = self.x_position - 1
        new_y = self.y_position
        if self.move_check(new_x, new_y):
            self.move(new_x, new_y)

    def move_north_west(self):
        new_x = self.x_position - 1
        new_y = self.y_position - 1
        if self.move_check(new_x, new_y):
            self.move(new_x, new_y)

    def move_south_west(self):
        new_x = self.x_position - 1
        new_y = self.y_position + 1
        if self.move_check(new_x, new_y):
            self.move(new_x, new_y)

    def move_south_east(self):
        new_x = self.x_position + 1
        new_y = self.y_position + 1
        if self.move_check(new_x, new_y):
            self.move(new_x, new_y)

    def move_north_east(self):
        new_x = self.x_position + 1
        new_y = self.y_position - 1
        if self.move_check(new_x, new_y):
            self.move(new_x, new_y)

    def draw_self(self):
        # self.window.addch(self.y_position, self.x_position, self.character)
        display.draw_entity(self.x_position, self.y_position, self.character, self.color_pair, self.window)

    def move_check(self, x, y):
        return display.check_walls_and_doors(x, y, self.floor_plan) and display.check_for_creatures(x, y)

    def look(self, floor_plan, hidden_map):
        seen_tiles = line_of_sight.compute((self.x_position, self.y_position), self.BASE_LINE_OF_SIGHT, floor_plan)
        return seen_tiles
