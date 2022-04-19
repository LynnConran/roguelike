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
        main_window = curses.newwin(MAIN_WINDOW_SIZE_Y, MAIN_WINDOW_SIZE_X, 1, 0)

        x = 'null'

        map_list = map.make_map()
        while x != 81:
            stdscr.clear()
            for y in range(MAIN_WINDOW_SIZE_Y - 1):
                for x in range(MAIN_WINDOW_SIZE_X):
                    main_window.addch(y, x, map_list[y][x])

            main_window.refresh()

            # curses.napms(5000)

            x = main_window.getch()

            stdscr.addstr(0, 0, "Key pressed: " + str(x))

            stdscr.refresh()



        end(stdscr)
