import creature
import global_variables


class Player(creature.Creature):
    CUSTOM_PAIR = 9

    BASE_LINE_OF_SIGHT = 5
    IS_PLAYER = True
    BASE_HEALTH = 10  # Replace later once stats exist

    def __init__(self, x_position, y_position, dungeon_level, floor_plan, creature_list, window, top, bottom,
                 color_code=(0, 0, 1000)):
        super().__init__(x_position, y_position, floor_plan, creature_list, self, window, '@', color_code)
        self.dungeon_level = dungeon_level
        self.top = top
        self.bottom = bottom
        # self.screen = screen
        self.is_seen = True
        self.top_string = ''
        self.bottom_messages = []
        self.update_bottom()

    def see_creatures(self, visible_tiles):
        for i in self.creature_list:
            i.is_seen = i.get_x_and_y() in visible_tiles

    def hit_wall(self):  # Designed to be called if the player walked into a wall
        self.top_string += "Bonk! "
        # self.screen.refresh()

    def update_bottom(self):
        self.bottom_messages = []
        self.bottom_messages.append((0, 0, "Dungeon Level: " + str(self.dungeon_level)))
        self.bottom_messages.append((0, 30, "HP(" + str(self.current_health) + ")"))

    def print_strings(self):
        # self.top.clear()
        # self.bottom.clear()
        # self.top.refresh()
        # self.bottom.refresh()
        self.top.addstr(0, 0, self.top_string)
        self.top_string = ''
        # self.bottom.addstr(0, 0, self.bottom_string)
        for string in self.bottom_messages:
            self.bottom.addstr(string[0], string[1], string[2])
        # self.screen.refresh()
        self.top.refresh()
        self.bottom.refresh()
        # self.window.refresh()

    def address_staircase(self, upstairs):
        if upstairs:
            self.top_string += "There is an upwards staircase here. "
        else:
            self.top_string += "There is a downwards staircase here. "

    def print_attack_message(self, instigator, critter, was_kill):
        if instigator.IS_PLAYER:
            if was_kill:
                # self.screen.addstr(0, 0, "You kill the " + critter.CLASS_NAME + "!")
                self.top_string += "You kill the " + critter.CLASS_NAME + "! "
            else:
                # self.screen.addstr(0, 0, "You hit the " + critter.CLASS_NAME + ", it has " +
                # str(critter.current_health) + " health remaining.")
                self.top_string += "You hit the " + critter.CLASS_NAME + ", it has " + str(critter.current_health) \
                                   + " health remaining. "
        else:
            if was_kill:
                if critter.IS_PLAYER:
                    self.top_string += "The " + instigator.CLASS_NAME + " hits you! You die... "
                else:
                    self.top_string += "The " + instigator.CLASS_NAME + " kills the " + critter.CLASS_NAME + "! "
            else:
                if critter.IS_PLAYER:
                    self.top_string += "The " + instigator.CLASS_NAME + " hits you! "
                else:
                    self.top_string += "The " + instigator.CLASS_NAME + " hits the " + critter.CLASS_NAME + "! "
        # self.screen.refresh()
