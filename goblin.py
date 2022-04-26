import creature


class Goblin(creature.Creature):

    BASE_LINE_OF_SIGHT = 3
    CLASS_NAME = "Goblin"
    BASE_HEALTH = 3

    def __init__(self, x_position, y_position, floor_plan, creature_list, player, window, screen):
        super().__init__(x_position, y_position, floor_plan, creature_list, player, window, screen, 'g', 2)
