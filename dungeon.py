import map
import global_variables

MAX_X = global_variables.MAIN_WINDOW_SIZE_X
MAX_Y = global_variables.MAIN_WINDOW_SIZE_Y
# MAX_X = 80
# MAX_Y = 26


def make_maps(num_maps, file_name, offset=0):
    map_list = []
    for i in range(num_maps):
        map_list.append(map.make_map())
    for i in range(len(map_list)):
        save_map(map_list[i][0], map_list[i][1], file_name, i + offset)


def save_map(level_map: list, hidden_map: list, file_name: str, line_number: int):
    current_character = level_map[0][0]
    current_boolean = hidden_map[0][0]

    level_count = 0
    level_str = ""

    hidden_str = ''
    hidden_count = 0

    for y in range(len(level_map)):
        for x in range (len(level_map[0])):
            if level_map[y][x] == current_character:
                level_count += 1
            else:
                level_str += current_character + str(level_count) + ' '
                current_character = level_map[y][x]
                level_count = 1
            if hidden_map[y][x] == current_boolean:
                hidden_count += 1
            else:
                hidden_str += str(int(current_boolean)) + ':' + str(hidden_count) + ' '
                # if current_boolean:
                #     hidden_str += '1:' + str(hidden_count) + '
                # else:
                #     hidden_str += '0:' + str(hidden_count)
                current_boolean = not current_boolean
                hidden_count = 1
    level_str += current_character + str(level_count) + ' \n'
    hidden_str += str(int(current_boolean)) + ':' + str(hidden_count) + ' \n'
    with open(file_name, 'r') as file:
        data = file.readlines()
    with open(file_name, 'w') as file:
        for i in range(len(data)):
            if i % 2 == 1:
                continue
            if i == line_number * 2:
                file.write(level_str)
                file.write(hidden_str)
            else:
                file.write(data[i])
                file.write(data[i + 1])
        if len(data) <= line_number * 2:
            file.write(level_str)
            file.write(hidden_str)
        # file.write(level_str)
        # file.write(hidden_str)


def read_map(level_file: str, line_number):
    level_list = []
    hidden_list = []

    for y in range(MAX_Y):
        level_sub_list = []
        hidden_sub_list = []
        for x in range(MAX_X):
            level_sub_list.append(' ')
            hidden_sub_list.append(False)
        level_list.append(level_sub_list)
        hidden_list.append(hidden_sub_list)

    with open(level_file, 'r') as file:
        data = file.readlines()

    level = data[line_number * 2]
    hidden = data[line_number * 2 + 1]
    level_index = 0
    level_count = 0
    while level_index < len(level) - 1:
        current_character = level[level_index]
        next_space = level.find(" ", level_index)
        number_to_repeat = int(level[level_index + 1:next_space])
        for i in range(number_to_repeat):
            level_list[int((i + level_count) / MAX_X)][(i + level_count) % MAX_X] = current_character
        level_count += number_to_repeat
        level_index = next_space + 1

    hidden_index = 0
    hidden_count = 0
    while hidden_index < len(hidden) - 1:
        current_boolean = bool(int(hidden[hidden_index]))
        next_colon = hidden.find(':', hidden_index)
        next_space = hidden.find(' ', hidden_index)
        number_to_repeat = int(hidden[next_colon + 1:next_space])
        for i in range(number_to_repeat):
            hidden_list[int((i + hidden_count) / MAX_X)][(i + hidden_count) % MAX_X] = current_boolean
        hidden_count += number_to_repeat
        hidden_index = next_space + 1

    return level_list, hidden_list


def check_for_end(level, file_name):
    with open(file_name, 'r') as file:
        data = file.readlines()
    return level * 2 >= len(data)

# if __name__ == '__main__':
#     hidden = []
#
#     for y in range(26):
#         temp_list = []
#         for x in range(80):
#             temp_list.append(False)
#         hidden.append(temp_list)
#
#     hidden[1][1] = True
#
#     level_map_one = map.make_map()
#     save_map(level_map_one, hidden, "test.txt", 0)
#
#     level_map_two = map.make_map()
#     save_map(level_map_two, hidden, 'test.txt', 1)
#
#     new_level, new_hidden = read_map("test.txt", 0)
#
#     print(str(level_map_one == new_level) + ' ' + str(hidden == new_hidden))
