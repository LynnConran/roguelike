import display, random

MAX_X = display.MAIN_WINDOW_SIZE_X
MAX_Y = display.MAIN_WINDOW_SIZE_Y

ROOM_MINIMUM_X = 5
ROOM_MINIMUM_Y = 3
ROOM_MAXIMUM_X = 11
ROOM_MAXIMUM_Y = 8

ROOM_DISTANCE = 3

NUM_ROOMS = 8

rooms = []


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

    for i in range(NUM_ROOMS):
        place_room(rows)

    return rows


def place_room(rows, recursive_count=0):
    if recursive_count > 15:
        return

    room_x_length = random.randint(0, ROOM_MAXIMUM_X - ROOM_MINIMUM_X) + ROOM_MINIMUM_X
    room_y_length = random.randint(0, ROOM_MAXIMUM_Y - ROOM_MINIMUM_Y) + ROOM_MINIMUM_Y

    room_x_position = random.randint(1, MAX_X - room_x_length - 1)
    room_y_position = random.randint(1, MAX_Y - room_y_length - 2)

    if check_room(room_x_length, room_y_length, room_x_position, room_y_position, rows):
        for y in range(room_y_length):
            for x in range(room_x_length):
                rows[y + room_y_position][x + room_x_position] = '_'
        rooms.append((room_x_length, room_y_length, room_x_position, room_y_position))
    else:
        place_room(rows, recursive_count + 1)
        return


def check_room(x_len, y_len, x_pos, y_pos, rows):
    for y in range(y_pos - ROOM_DISTANCE, y_len + y_pos + ROOM_DISTANCE):
        for x in range(x_pos - ROOM_DISTANCE, x_len + x_pos + ROOM_DISTANCE):
            if x < 1 or x > MAX_X - 1 or y < 1 or y > MAX_Y - 1:
                continue
            if rows[y][x] != "#":
                return False
    return True


def make_corridors(rows):
    for i in range(len(rooms)):
        goal_room = random.randint(0, len(rooms))
        while goal_room == i:
            goal_room = random.randint(0, len(rooms))

        west_east = rooms[i](0) < rooms[goal_room](0) # west = 0, east = 1
        north_south = rooms[i](1) < rooms[goal_room](1) # north = 0, east = 1

        if rooms[i](0) - rooms[goal_room](0) < ROOM_MINIMUM_X:
            north_south = -1
        if rooms[i](1) - rooms[goal_room](1) < ROOM_MINIMUM_Y:
            west_east = -1

        if random.random() > .5 and west_east > -1 or north_south < 0:  # starting on the east west axis
            x_start = rooms[i](0) - 1 + (west_east * (rooms[i](2) + 1))  # Works out to either 0 or the east edge
            y_start = rooms[i](1) + random.randint(0, rooms[i][3])

            if north_south > -1:
                y_end = rooms[goal_room](1) - 1 + (west_east * (rooms[goal_room](3) + 1))
                x_end = rooms[goal_room](0) + random.randint(0, rooms[goal_room][2])
            else:
                x_end = rooms[goal_room](0) - 1 + (west_east * (rooms[goal_room](2) + 1))
                y_end = rooms[goal_room](1) + random.randint(0, rooms[goal_room][3])
        else:                                                           # starting on the south north axis
            y_start = rooms[i](1) - 1 + (north_south * (rooms[i](3) + 1))  # Works out to either 0 or the south edge
            x_start = rooms[i](0) + random.randint(0, rooms[i][2])
            if west_east > -1:
                x_end = rooms[goal_room](0) - 1 + (north_south * (rooms[goal_room](2) + 1))
                y_end = rooms[goal_room](1) + random.randint(0, rooms[goal_room][3])
            else:
                y_end = rooms[goal_room](1) - 1 + (north_south * (rooms[goal_room](3) + 1))
                x_end = rooms[goal_room](0) + random.randint(0, rooms[goal_room][2])
