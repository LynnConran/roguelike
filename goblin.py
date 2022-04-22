import creature

class Goblin(creature.Creature):

    BASE_LINE_OF_SIGHT = 3

    def __init__(self, x_position, y_position, floor_plan, window):
        super().__init__(x_position, y_position, floor_plan, window, 'g', 2)