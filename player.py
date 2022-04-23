import creature
import math


# def unhide(seen_tiles, hidden_list):
#     for i in seen_tiles:
#         hidden_list[i[1]][i[0]] = True
#     return seen_tiles


class Player(creature.Creature):

    BASE_LINE_OF_SIGHT = 5
    SIGHT_LEEWAY = 0.4  # How fuzzy the distance is allowed to be. Pulled right out of a hat.
    IS_PLAYER = True

    def __init__(self, x_position, y_position, floor_plan, creature_list, window, color_pair=0):
        super().__init__(x_position, y_position, floor_plan, creature_list, window, '@', color_pair)


    #     x_max = len(self.floor_plan[0])
    #     y_max = len(self.floor_plan)
    #
    #     seen_list = []
    #
    #     for y in range(self.y_position - self.BASE_LINE_OF_SIGHT, self.y_position + self.BASE_LINE_OF_SIGHT + 1):
    #         for x in range(self.x_position - self.BASE_LINE_OF_SIGHT, self.x_position + self.BASE_LINE_OF_SIGHT + 1):
    #             if x < 0 or y < 0 or x >= x_max or y >= y_max:
    #                 continue
    #             # Add looking logic here
    #
    #             # Using recursive shadowcasting to calculate line of sight
    #     # Actually, credit should go to the writer of http://www.adammil.net/blog/v125_Roguelike_Vision_Algorithms.html
    #             distance = math.dist((x, y), (self.x_position, self.y_position))
    #             if distance <= self.BASE_LINE_OF_SIGHT + self.SIGHT_LEEWAY:
    #                 seen_list.append((x, y))
    #
    #     return seen_list
