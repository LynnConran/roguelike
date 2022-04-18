import curses
import map

MAIN_WINDOW_SIZE_X = 80
MAIN_WINDOW_SIZE_Y = 26

def end(scr):
    curses.nocbreak()
    scr.keypad(False)
    curses.echo()
    curses.curs_set(1)

    curses.endwin()


if __name__ == '__main__':
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    curses.curs_set(0)

    num_rows, num_columns = stdscr.getmaxyx()

    if num_rows < MAIN_WINDOW_SIZE_Y - 1 or num_columns < MAIN_WINDOW_SIZE_X:
        stdscr.addstr(0, 0, "Screen too small, aborting")
        stdscr.refresh()
        curses.napms(2000)
        end(stdscr)
        # curses.resizeterm(MAIN_WINDOW_SIZE_Y - 1, MAIN_WINDOW_SIZE_X)

    else:
        main_window = curses.newwin(MAIN_WINDOW_SIZE_Y, MAIN_WINDOW_SIZE_X, 0, 0)
        # main_window.addstr(0, 1, "This string gets printed at position (0, 0)")
        # main_window.addstr(3, 1, "Try Russian text: Привет")  # Python 3 required for unicode
        # main_window.addstr(4, 4, "X")
        # main_window.addch(5, 5, "Y")
        # main_window.addstr(11, 70, "long string seeing if it wraps around")

        map_list = map.make_map()

        for y in range(MAIN_WINDOW_SIZE_Y - 1):
            for x in range(MAIN_WINDOW_SIZE_X):
                main_window.addch(y, x, map_list[y][x])

        # for y in range(MAIN_WINDOW_SIZE_Y - 1):
        #     for x in range(MAIN_WINDOW_SIZE_X):
        #         main_window.addstr(y, x, "#")

        # for y in range(10):
        #     for x in range(15):
        #         main_window.addch(y, x, map_list[y - 1][x - 1])

        # for y in range(10):
        #     for x in range(15):
        #         main_window.addch(y, x, str(y))

        # main_window.addch(0, 0, map_list[0][0])

        main_window.refresh()

        curses.napms(5000)

        end(stdscr)
