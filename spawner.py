import goblin  # Will import every creature. No, really. I'll remove this as soon as I have a better idea


def create(creature_type, x_position, y_position, floor_plan, creature_list, player, window, assigned_pair):
    if creature_type == 'goblin':
        return goblin.Goblin(x_position, y_position, floor_plan, creature_list, player, window, assigned_pair)
    elif creature_type == 'orc':
        pass  # you get the idea
