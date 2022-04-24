import curses
import global_variables
import line_of_sight


def check_walls_and_doors(x, y, floor_plan):
    if x < 0 or x >= global_variables.MAIN_WINDOW_SIZE_X or y < 0 or y >= global_variables.MAIN_WINDOW_SIZE_Y \
            or floor_plan[y][x] == '#':
        return False
    return True


class Creature:
    BASE_LINE_OF_SIGHT = 4
    IS_PLAYER = False  # Overwritten by player, if I understand inheritance properly
    CLASS_NAME = "?"
    BASE_HEALTH = 1

    def __init__(self, x_position, y_position, floor_plan, creature_list, window, screen, character, color_pair=0):
        self.x_position = x_position
        self.y_position = y_position
        self.floor_plan = floor_plan
        self.creature_list = creature_list
        self.window = window
        self.screen = screen
        self.character = character
        self.color_pair = color_pair
        self.current_health = self.BASE_HEALTH

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
        # display.draw_entity(self.x_position, self.y_position, self.character, self.color_pair, self.window)
        self.window.addch(self.y_position, self.x_position, self.character, curses.color_pair(self.color_pair))

    def move_check(self, x, y):
        # return display.check_walls_and_doors(x, y, self.floor_plan) \
        #        and display.check_for_creatures(x, y, self.creature_list)
        if not check_walls_and_doors(x, y, self.floor_plan):
            if self.IS_PLAYER:
                self.hit_wall()
            return False
        if not self.check_for_creatures(x, y):
            self.interact((x, y))
            return False
        return True

    def check_for_creatures(self, x_pos, y_pos):
        destination = (x_pos, y_pos)
        for critter in self.creature_list:
            if destination == critter.get_x_and_y():
                return False
        return True

    def look(self, floor_plan):
        seen_tiles = line_of_sight.compute((self.x_position, self.y_position), self.BASE_LINE_OF_SIGHT, floor_plan)
        return seen_tiles

    def get_x_and_y(self):
        return self.x_position, self.y_position

    def calculate_damage(self, critter):
        return 1

    def hit_wall(self):  # Designed to be called if the player walked into a wall
        self.screen.addstr(0, 0, "Bonk!")
        self.screen.refresh()

    def equals(self, critter):
        return self.get_x_and_y() == critter.get_x_and_y()

    def die(self):
        if not self.IS_PLAYER:
            self.creature_list.remove(self)
        else:
            pass

    def attack(self, critter):
        damage = self.calculate_damage(critter)
        critter.current_health -= damage
        is_critter_killed = critter.current_health < 1
        if critter.current_health < 1:
            critter.die()
        self.print_attack_message(critter, is_critter_killed)

    def print_attack_message(self, critter, was_kill):
        if self.IS_PLAYER:
            if was_kill:
                self.screen.addstr(0, 0, "You kill the " + critter.CLASS_NAME + "!")
            else:
                self.screen.addstr(0, 0, "You hit the " + critter.CLASS_NAME + ", it has " + str(critter.current_health)
                                   + " health remaining.")
        else:
            pass
        self.screen.refresh()

    def change_floor_plan(self, plan):
        self.floor_plan = plan

    def interact(self, position):
        if self.IS_PLAYER:
            my_creature = Creature(0, 0, [], [], 'null', 'null', '?')
            for i in self.creature_list:
                if position == i.get_x_and_y():
                    my_creature = i
                    break
            self.attack(my_creature)

        else:
            pass
