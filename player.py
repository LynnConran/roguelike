import creature


class Player(creature.Creature):

    BASE_LINE_OF_SIGHT = 5
    IS_PLAYER = True
    BASE_HEALTH = 10  # Replace later once stats exist

    def __init__(self, x_position, y_position, floor_plan, creature_list, window, screen, color_pair=0):
        super().__init__(x_position, y_position, floor_plan, creature_list, self, window, screen, '@', color_pair)
        self.is_seen = True

    def see_creatures(self, visible_tiles):
        for i in self.creature_list:
            i.is_seen = i.get_x_and_y() in visible_tiles
