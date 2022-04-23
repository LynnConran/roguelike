import creature


class Player(creature.Creature):

    BASE_LINE_OF_SIGHT = 5
    IS_PLAYER = True
    BASE_HEALTH = 10  # Replace later once stats exist

    def __init__(self, x_position, y_position, floor_plan, creature_list, window, color_pair=0):
        super().__init__(x_position, y_position, floor_plan, creature_list, window, '@', color_pair)
