import creature

class Goblin(creature.Creature):

    def __init__(self, x_position, y_position, floor_plan, window):
        super().__init__(x_position, y_position, floor_plan, window, 'g')