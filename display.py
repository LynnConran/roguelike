import curses
import global_variables
import player
import random
import goblin
import dungeon

MINIMUM_WINDOW_SIZE_X = global_variables.MINIMUM_WINDOW_SIZE_X
MINIMUM_WINDOW_SIZE_Y = global_variables.MINIMUM_WINDOW_SIZE_Y
MAIN_WINDOW_SIZE_X = global_variables.MAIN_WINDOW_SIZE_X
MAIN_WINDOW_SIZE_Y = global_variables.MAIN_WINDOW_SIZE_Y

stdscr = curses.initscr()
# hidden = []
# floor_plan = map.make_map()


def end(scr):
    curses.nocbreak()
    scr.keypad(False)
    curses.echo()
    curses.curs_set(1)

    curses.endwin()


def make_player_coords():
    x = random.randint(0, MAIN_WINDOW_SIZE_X - 1)
    y = random.randint(0, MAIN_WINDOW_SIZE_Y - 1)

    while floor_plan[y][x] != '.':
        x = random.randint(0, MAIN_WINDOW_SIZE_X - 1)
        y = random.randint(0, MAIN_WINDOW_SIZE_Y - 1)

    return x, y


def make_monster_coords():
    x = random.randint(0, MAIN_WINDOW_SIZE_X - 1)
    y = random.randint(0, MAIN_WINDOW_SIZE_Y - 1)

    while floor_plan[y][x] != '.':
        x = random.randint(0, MAIN_WINDOW_SIZE_X - 1)
        y = random.randint(0, MAIN_WINDOW_SIZE_Y - 1)

    return x, y


def change_level(floor_plan, hidden_list, level_string):
    for y in range(MAIN_WINDOW_SIZE_Y):
        for x in range(MAIN_WINDOW_SIZE_X):
            index = y * MAIN_WINDOW_SIZE_X + x
            if not hidden_list[y][x]:
                level_string = level_string[:index] + ' ' + level_string[index + 1:]
            else:
                level_string = level_string[:index] + floor_plan[y][x] + level_string[index + 1:]
    return level_string


def unhide(hidden_list, seen_tiles, floor_plan, level_string):
    for i in seen_tiles:
        if not hidden_list[i[1]][i[0]]:
            index = i[1] * MAIN_WINDOW_SIZE_X + i[0]
            level_string = level_string[:index] + floor_plan[i[1]][i[0]] + level_string[index+1:]
            hidden_list[i[1]][i[0]] = True
    return level_string, hidden_list


def reveal_all(hidden_list, floor_plan, level_string):
    big_ol_list = []
    for y in range(len(hidden_list)):
        for x in range(len(hidden_list[0])):
            big_ol_list.append((x, y))
    return unhide(hidden_list, big_ol_list, floor_plan, level_string)


def make_pairs():
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_color(curses.COLOR_CYAN, 0, 0, 1000)
    curses.init_pair(8, curses.COLOR_CYAN, curses.COLOR_BLACK)


def game_over():
    stdscr.addstr(0, 0, "Lmao, you literally died")


def make_string():
    my_str = ""
    for y in range(MAIN_WINDOW_SIZE_Y):
        temp_str = ''
        for x in range(MAIN_WINDOW_SIZE_X):
            temp_str += " "
        my_str += temp_str
    return my_str


def check_on_upstairs():
    return floor_plan[player.y_position][player.x_position] == '<'


def check_on_downstairs():
    return floor_plan[player.y_position][player.x_position] == '>'


def move_upstairs(level):  # I expect to put more logic here eventually
    if level == 1:
        stdscr.addstr(0, 0, "Are you sure?")
        stdscr.refresh()
        return level, False
    else:
        level -= 1
    return level, True


def move_downstairs(level, file_name='dungeon.txt'):
    level += 1
    if dungeon.check_for_end(level - 1, file_name):
        dungeon.make_maps(1, file_name, level - 1)
    return level, True


def place_player(going_down, floor_plan):
    if going_down:
        goal = '<'
    else:
        goal = '>'
    for y in range(len(floor_plan)):
        for x in range(len(floor_plan[0])):
            if floor_plan[y][x] == goal:
                return x, y
    return -1, -1


# def place_bottom_messages():
#     stdscr.addstr(MINIMUM_WINDOW_SIZE_Y - 2, 0, "Dungeon Level: " + str(dungeon_level))


if __name__ == '__main__':
    # global hidden

    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    curses.start_color()
    curses.curs_set(0)
    make_pairs()

    num_rows, num_columns = stdscr.getmaxyx()

    if not curses.has_colors():
        stdscr.addstr(0, 0, "no colors, aborting")
        stdscr.refresh()
        curses.napms(2000)
        end(stdscr)

    elif num_rows < MINIMUM_WINDOW_SIZE_Y or num_columns < MINIMUM_WINDOW_SIZE_X:
        stdscr.addstr(0, 0, "Screen too small, aborting")
        stdscr.refresh()
        curses.napms(2000)
        end(stdscr)
        # curses.resizeterm(MAIN_WINDOW_SIZE_Y - 1, MAIN_WINDOW_SIZE_X)

    else:
        main_window = curses.newwin(MAIN_WINDOW_SIZE_Y + 1, MAIN_WINDOW_SIZE_X, 2, 0)
        messages_window = curses.newwin(2, MAIN_WINDOW_SIZE_X, 0, 0)
        bottom_window = curses.newwin(10, MAIN_WINDOW_SIZE_X, MAIN_WINDOW_SIZE_Y + 2, 0)

        # floor_plan, hidden = map.make_map()

        with open('dungeon.txt', 'w') as file:
            pass

        dungeon.make_maps(3, 'dungeon.txt')

        floor_plan, hidden = dungeon.read_map('dungeon.txt', 0)

        dungeon_level = 1

        creature_list = []

        level_string = make_string()

        x = 'null'

        player_x, player_y = place_player(True, floor_plan)

        goblin_x, goblin_y = make_monster_coords()

        player = player.Player(player_x, player_y, dungeon_level, floor_plan, creature_list, main_window,
                               messages_window, bottom_window)

        goblin = goblin.Goblin(goblin_x, goblin_y, floor_plan, creature_list, player, main_window, 1)

        creature_list.append(goblin)

        # place_bottom_messages()
        player.print_strings()

        stdscr.refresh()

        while x != 81:
            stdscr.clear()
            main_window.clear()

            if x == 49 or x == 98:    # = 1 or n
                player.move_south_west()
            elif x == 50 or x == 106:  # = 2 or j
                player.move_south()
            elif x == 51 or x == 110:  # = 3 or n
                player.move_south_east()
            elif x == 52 or x == 104:  # = 4 or h
                player.move_west()
            elif x == 53:  # = 5
                pass
            elif x == 54 or x == 108:  # = 6 or l
                player.move_east()
            elif x == 55 or x == 121:  # = 7 or y
                player.move_north_west()
            elif x == 56 or x == 107:  # = 8 or k
                player.move_north()
            elif x == 57 or x == 117:  # = 9 or u
                player.move_north_east()
            elif x == 92:  # = \
                level_string, hidden, = reveal_all(hidden, floor_plan, level_string)
            elif x == 60:  # <
                if check_on_upstairs():
                    dungeon.save_map(floor_plan, hidden, "dungeon.txt", dungeon_level - 1)
                    dungeon_level, has_moved = move_upstairs(dungeon_level)
                    if has_moved:
                        floor_plan, hidden = dungeon.read_map("dungeon.txt", dungeon_level - 1)
                        player.change_floor_plan(floor_plan)
                        player.print_strings()
                        for i in creature_list:
                            i.change_floor_plan(floor_plan)
                        level_string = change_level(floor_plan, hidden, level_string)
                        player.x_position, player.y_position = place_player(False, floor_plan)
                        player.dungeon_level = dungeon_level
                        player.update_bottom()
                        stdscr.refresh()
            elif x == 62:  # >
                if check_on_downstairs():
                    dungeon.save_map(floor_plan, hidden, "dungeon.txt", dungeon_level - 1)
                    dungeon_level, has_moved = move_downstairs(dungeon_level)
                    if has_moved:
                        floor_plan, hidden = dungeon.read_map("dungeon.txt", dungeon_level - 1)
                        player.change_floor_plan(floor_plan)
                        player.print_strings()
                        for i in creature_list:
                            i.change_floor_plan(floor_plan)
                        level_string = change_level(floor_plan, hidden, level_string)
                        player.x_position, player.y_position = place_player(True, floor_plan)
                        player.dungeon_level = dungeon_level
                        player.update_bottom()
                        stdscr.refresh()

            for i in creature_list:
                i.npc_move()
                # i.change_path()

            # seen_tiles = player.look()
            visible_tiles = player.look()
            player.see_creatures(visible_tiles)

            # for y in range(MAIN_WINDOW_SIZE_Y):
            #     for x in range(MAIN_WINDOW_SIZE_X):
            #         visible_tiles.append((x, y))

            level_string, hidden = unhide(hidden, visible_tiles, floor_plan, level_string)

            main_window.addstr(0, 0, level_string)

            player.draw_self()

            for i in creature_list:
                if (i.x_position, i.y_position) in visible_tiles:
                    i.draw_self()
            # goblin.draw_self()

            main_window.refresh()

            # curses.napms(5000)

            player.print_strings()

            x = main_window.getch()

            # stdscr.addstr(0, 0, "Key pressed: " + str(x))

            # place_bottom_messages()
            player.print_strings()

            stdscr.refresh()

        end(stdscr)
