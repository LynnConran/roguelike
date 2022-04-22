import curses
import map
import player
import random
import goblin

MAIN_WINDOW_SIZE_X = 80
MAIN_WINDOW_SIZE_Y = 26

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


def check_walls_and_doors(x, y, floor_plan):
    if x < 0 or x >= MAIN_WINDOW_SIZE_X or y < 0 or y >= MAIN_WINDOW_SIZE_Y or floor_plan[y][x] == '#':
        return False
    return True


def check_for_creatures(x_pos, y_pos):
    return True


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


def draw_entity(x, y, char, pair, screen):
    screen.addch(y, x, char, curses.color_pair(pair))


def make_pairs():
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)



def make_string():
    my_str = ""
    for y in range(MAIN_WINDOW_SIZE_Y):
        temp_str = ''
        for x in range(MAIN_WINDOW_SIZE_X):
            temp_str += " "
        my_str += temp_str
    return my_str


if __name__ == '__main__':
    # global hidden

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    curses.start_color()
    curses.curs_set(0)
    make_pairs()


    # make_hidden()
    # for y in range(len(map_list)):
    #     temp_list = []
    #     for x in range(len(map_list[0])):
    #         temp_list.append(False)
    #     hidden.append(temp_list)

    num_rows, num_columns = stdscr.getmaxyx()

    if not curses.has_colors():
        stdscr.addstr(0, 0, "no colors, aborting")
        stdscr.refresh()
        curses.napms(2000)
        end(stdscr)


    elif num_rows < MAIN_WINDOW_SIZE_Y or num_columns < MAIN_WINDOW_SIZE_X:
        stdscr.addstr(0, 0, "Screen too small, aborting")
        stdscr.refresh()
        curses.napms(2000)
        end(stdscr)
        # curses.resizeterm(MAIN_WINDOW_SIZE_Y - 1, MAIN_WINDOW_SIZE_X)

    else:
        main_window = curses.newwin(MAIN_WINDOW_SIZE_Y + 1, MAIN_WINDOW_SIZE_X, 1, 0)

        floor_plan = map.make_map()

        creature_list = []

        level_string = ''
        level_string += make_string()

        x = 'null'

        # Two-dimensional list of booleans, false means hidden, true means seen and therefore visible.
        hidden = []

        for y in range(MAIN_WINDOW_SIZE_Y):
            temp_list = []
            for x in range(MAIN_WINDOW_SIZE_X):
                temp_list.append(False)
            hidden.append(temp_list)

        player_x, player_y = make_player_coords()

        goblin_x, goblin_y = make_monster_coords()

        player = player.Player(player_x, player_y, floor_plan, main_window)

        goblin = goblin.Goblin(goblin_x, goblin_y, floor_plan, main_window)

        creature_list.append(goblin)

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
            elif x == 92:
                level_string, hidden, = reveal_all(hidden, floor_plan, level_string)

            # seen_tiles = player.look()
            visible_tiles = player.look(floor_plan, hidden)

            level_string, hidden = unhide(hidden, visible_tiles, floor_plan, level_string)

            # for i in seen_tiles:
            #     hidden[i[1]][i[0]] = True
            #
            # for y in range(MAIN_WINDOW_SIZE_Y - 1):
            #     for x in range(MAIN_WINDOW_SIZE_X):
            #         if hidden[y][x]:
            #             # if (x, y) in visible_tiles:
            #             #     main_window.addch(y, x, floor_plan[y][x], curses.color_pair(1))
            #             # else:
            #             main_window.addch(y, x, floor_plan[y][x])\

            main_window.addstr(0, 0, level_string)

            # for y in range(player.y_position - player.BASE_LINE_OF_SIGHT, player.y_position + player.BASE_LINE_OF_SIGHT):
            #     for x in range (player.x_position - player.BASE_LINE_OF_SIGHT, player.x_position + player.BASE_LINE_OF_SIGHT):
            #         if not (x < 0 or x >= MAIN_WINDOW_SIZE_X or y < 0 or y >= MAIN_WINDOW_SIZE_Y):
            #             if (x, y) in visible_tiles:
            #                 main_window.addch(y, x, floor_plan[y][x], curses.color_pair(1))

            # for i in visible_tiles:
            #     main_window.addch(i[1], i[0], floor_plan[i[1]][i[0]], curses.color_pair(1))

            player.draw_self()

            for i in creature_list:
                if (i.x_position, i.y_position) in visible_tiles:
                    i.draw_self()
            # goblin.draw_self()

            main_window.refresh()

            # curses.napms(5000)

            x = main_window.getch()

            stdscr.addstr(0, 0, "Key pressed: " + str(x))

            stdscr.refresh()

        end(stdscr)
