import display, random

MAX_X = display.MAIN_WINDOW_SIZE_X
MAX_Y = display.MAIN_WINDOW_SIZE_Y

ROOM_MINIMUM = 3
ROOM_MAXIMUM = 8


def make_map():
    # Currently a massive stub

    rows = []
    columns = []

    for y in range(MAX_Y):
        for x in range(MAX_X):
            columns.append('#')
        rows.append(columns)
        columns = []

    # file = "log.txt"
    # with open(file, "w") as my_file:
    #     my_file.writelines(str(rows))

    for i in range(15):
        place_room(rows)

    return rows


def place_room(rows):
    room_x_length = random.randint(0, ROOM_MAXIMUM - ROOM_MINIMUM) + ROOM_MINIMUM
    room_y_length = random.randint(0, ROOM_MAXIMUM - ROOM_MINIMUM) + ROOM_MINIMUM

    room_x_position = random.randint(1, MAX_X - room_x_length - 1)
    room_y_position = random.randint(1, MAX_Y - room_y_length - 2)

    if check_room(room_x_length, room_y_length, room_x_position, room_y_position, rows):
        for y in range(room_y_length):
            for x in range(room_x_length):
                rows[y + room_y_position][x + room_x_position] = '_'
    else:
        place_room(rows)
        return


def check_room(x_len, y_len, x_pos, y_pos, rows):
    for y in range(y_pos - 1, y_len + y_pos + 1):
        for x in range(x_pos - 1, x_len + x_pos + 1):
            if rows[y][x] != "#":
                return False
    return True
