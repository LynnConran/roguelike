import curses
import map
import player
import random

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


# def reveal(x, y):
#     # global hidden
#     if x < 0 or x >= MAIN_WINDOW_SIZE_X or y < 0 or y >= MAIN_WINDOW_SIZE_Y:
#         return
#     hidden[y][x] = True
#     # hidden[0][0] = True
#     # for y in range(MAIN_WINDOW_SIZE_Y):
#     #     for x in range(MAIN_WINDOW_SIZE_X):
#     #         hidden[y][x] = True


def check_walls_and_doors(x, y, floor_plan):
    if x < 0 or x >= MAIN_WINDOW_SIZE_X or y < 0 or y >= MAIN_WINDOW_SIZE_Y or floor_plan[int(y)][int(x)] == '#':
        return False
    return True


def check_for_creatures(x_pos, y_pos):
    return True


# def make_hidden():
#     global hidden
#     hidden = []
#     for y in range(MAIN_WINDOW_SIZE_Y):
#         temp_list = []
#         for x in range(MAIN_WINDOW_SIZE_X):
#             temp_list.append(False)
#         hidden.append(temp_list)


# def make_map():
#     global map_list
#     map_list = map.make_map()


if __name__ == '__main__':
    # global hidden

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    curses.curs_set(0)

    # make_hidden()
    # for y in range(len(map_list)):
    #     temp_list = []
    #     for x in range(len(map_list[0])):
    #         temp_list.append(False)
    #     hidden.append(temp_list)

    num_rows, num_columns = stdscr.getmaxyx()

    if num_rows < MAIN_WINDOW_SIZE_Y or num_columns < MAIN_WINDOW_SIZE_X:
        stdscr.addstr(0, 0, "Screen too small, aborting")
        stdscr.refresh()
        curses.napms(2000)
        end(stdscr)
        # curses.resizeterm(MAIN_WINDOW_SIZE_Y - 1, MAIN_WINDOW_SIZE_X)

    else:
        main_window = curses.newwin(MAIN_WINDOW_SIZE_Y, MAIN_WINDOW_SIZE_X, 1, 0)

        floor_plan = map.make_map()

        x = 'null'

        # Two-dimensional list of booleans, false means hidden, true means seen and therefore visible.
        hidden = []

        for y in range(MAIN_WINDOW_SIZE_Y):
            temp_list = []
            for x in range(MAIN_WINDOW_SIZE_X):
                temp_list.append(False)
            hidden.append(temp_list)

        player_x, player_y = make_player_coords()

        player = player.Player(player_x, player_y, floor_plan, main_window)

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

            # seen_tiles = player.look()
            hidden = player.look(floor_plan, hidden)

            # for i in seen_tiles:
            #     hidden[i[1]][i[0]] = True

            for y in range(MAIN_WINDOW_SIZE_Y - 1):
                for x in range(MAIN_WINDOW_SIZE_X):
                    if hidden[y][x]:
                        main_window.addch(y, x, floor_plan[y][x])

            player.draw_self()

            main_window.refresh()

            # curses.napms(5000)

            x = main_window.getch()

            stdscr.addstr(0, 0, "Key pressed: " + str(x))

            stdscr.refresh()

        end(stdscr)
