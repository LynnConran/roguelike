import curses
import global_variables
import line_of_sight
import path_finding
import random
import math


class Creature:

    BASE_LINE_OF_SIGHT = 4
    IS_PLAYER = False  # Overwritten by player, if I understand inheritance properly
    CLASS_NAME = "?"
    BASE_HEALTH = 1
    CUSTOM_PAIR = 1

    def __init__(self, x_position, y_position, floor_plan, creature_list, player, window, character,
                 color_code=(0, 0, 0)):
        self.x_position = x_position
        self.y_position = y_position
        self.floor_plan = floor_plan
        self.creature_list = creature_list
        self.window = window
        self.character = character
        self.color_code = color_code
        self.current_health = self.BASE_HEALTH
        self.is_seen = False
        self.player = player
        self.path = []
        self.target = self.player
        self.stair_list = self.get_stair_locations()

    def move(self, x_pos, y_pos):
        self.x_position = x_pos
        self.y_position = y_pos
        if self.IS_PLAYER:
            self.check_on_stairs()

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

    def get_stair_locations(self):
        stair_list = []
        for y in range(len(self.floor_plan)):
            for x in range(len(self.floor_plan[0])):
                if self.floor_plan[y][x] == '<' or self.floor_plan[y][x] == '>':
                    stair_list.append((x, y))
        return stair_list

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

    def define_color(self):
        curses.init_color(self.CUSTOM_PAIR, self.color_code[0], self.color_code[1], self.color_code[2])
        curses.init_pair(self.CUSTOM_PAIR, self.CUSTOM_PAIR, curses.COLOR_BLACK)  # Color and pair number are the same
        # in order to simplify matters

    def draw_self(self):
        self.define_color()  # When this was put in __init__, the goblin disappeared when attacked. Reasons unknown.
        self.window.addch(self.y_position, self.x_position, self.character, curses.color_pair(self.CUSTOM_PAIR))

    def check_walls_and_doors(self, x, y):
        return not (x < 0 or x >= global_variables.MAIN_WINDOW_SIZE_X or y < 0
                    or y >= global_variables.MAIN_WINDOW_SIZE_Y or self.floor_plan[y][x] == '#')

    def move_check(self, x, y):
        if not self.check_walls_and_doors(x, y):
            if self.IS_PLAYER:
                self.player.hit_wall()
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
        if destination == self.player.get_x_and_y():
            return False
        return True

    def look(self):
        return line_of_sight.compute((self.x_position, self.y_position), self.BASE_LINE_OF_SIGHT, self.floor_plan)

    def has_seen_target(self):
        seen_tiles = self.look()
        return self.target.get_x_and_y() in seen_tiles

    def get_x_and_y(self):
        return self.x_position, self.y_position

    def calculate_damage(self, critter):
        return 1

    def change_path(self):
        if len(self.path) < 1 or self.path[len(self.path) - 1] != self.player.get_x_and_y():
            self.path = path_finding.search(self.floor_plan, self.creature_list, self.player.get_x_and_y(),
                                            self.get_x_and_y(), self.player.get_x_and_y())
            if self.path == "Not Found":
                self.path = []

    def npc_move(self):
        sees_target = False
        if math.dist(self.get_x_and_y(), self.target.get_x_and_y()) <= self.BASE_LINE_OF_SIGHT:
            sees_target = self.has_seen_target()
        if len(self.path) >= 1:
            if self.target.get_x_and_y() == self.path[len(self.path) - 1]:
                self.deliberate_move()
            else:
                if sees_target:
                    self.change_path()
                    self.deliberate_move()
                else:
                    self.path.clear()
                    self.random_move()
        elif sees_target:
            self.change_path()
            if len(self.path) >= 1:  # In case they see the player but can't reach them
                self.deliberate_move()
        else:
            self.random_move()

    def deliberate_move(self):
        coords = self.path[0]
        if coords[0] < self.x_position:
            if coords[1] < self.y_position:
                self.move_north_west()
            elif coords[1] == self.y_position:
                self.move_west()
            elif coords[1] > self.y_position:
                self.move_south_west()
        elif coords[0] == self.x_position:
            if coords[1] < self.y_position:
                self.move_north()
            elif coords[1] == self.y_position:
                pass
            elif coords[1] > self.y_position:
                self.move_south()
        elif coords[0] > self.x_position:
            if coords[1] < self.y_position:
                self.move_north_east()
            elif coords[1] == self.y_position:
                self.move_east()
            elif coords[1] > self.y_position:
                self.move_south_east()
        del self.path[0]

    def random_move(self):
        random_number = random.random()
        if random_number < .111:
            self.move_north()
        elif random_number < .222:
            self.move_north_east()
        elif random_number < .333:
            self.move_east()
        elif random_number < .444:
            self.move_south_east()
        elif random_number < .555:
            pass
        elif random_number < .666:
            self.move_south()
        elif random_number < .777:
            self.move_south_west()
        elif random_number < .888:
            self.move_west()
        else:
            self.move_north_west()

    def die(self):
        if not self.IS_PLAYER:
            self.creature_list.remove(self)
        else:
            pass

    def attack(self, critter):
        damage = self.calculate_damage(critter)
        critter.current_health -= damage
        if critter == self.player:
            self.player.update_bottom()
        is_critter_killed = critter.current_health < 1
        if is_critter_killed:
            critter.die()
        if self.is_seen:
            self.player.print_attack_message(self, critter, is_critter_killed)

    def change_floor_plan(self, plan):
        self.floor_plan = plan
        self.stair_list = self.get_stair_locations()

    def change_entity_list(self, entities):
        self.creature_list = entities

    def check_on_stairs(self):
        if self.get_x_and_y() in self.stair_list:
            if self.floor_plan[self.y_position][self.x_position] == '<':
                self.player.address_staircase(True)
            else:
                self.player.address_staircase(False)

    def interact(self, position):
        if self.IS_PLAYER:
            my_creature = Creature(0, 0, [], [], 'null', 'null', 'null', '?')
            for i in self.creature_list:
                if position == i.get_x_and_y():
                    my_creature = i
                    break
            self.attack(my_creature)

        else:
            if position == self.player.get_x_and_y():
                my_creature = self.player
            else:
                my_creature = Creature(0, 0, [], [], 'null', 'null', 'null', '?')
                for i in self.creature_list:
                    if position == i.get_x_and_y():
                        my_creature = i
                        break
            self.attack(my_creature)
