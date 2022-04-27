import creature


class Goblin(creature.Creature):

    BASE_LINE_OF_SIGHT = 3
    CLASS_NAME = "Goblin"
    BASE_HEALTH = 3

    COLOR = (0, 1000, 0)

    def __init__(self, x_position, y_position, floor_plan, creature_list, player, window, assigned_pair):
        super().__init__(x_position, y_position, floor_plan, creature_list, player, window, 'g', self.COLOR)
        self.CUSTOM_PAIR = assigned_pair
