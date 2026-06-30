#!/bin/python

from typing import Tuple, List, Iterator, Dict
from dataclasses import dataclass
from copy import deepcopy

BOARD_SIZE = 3

TILE_RED = "r"
TILE_BLACK = "b"
TILE_WHITE = "w"
TILE_GREY = "g"
TILE_GREEN = "G"
TILE_ORANGE = "o"
TILE_VIOLET = "v"
TILE_YELLOW = "y"
TILE_PINK = "p"
TILE_BLUE = "B"

# (0, 0), (1, 0), (2, 0)
# (0, 1), (1, 1), (2, 1)
# (0, 2), (1, 2), (2, 2)


def surrounding(pos: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    """
    return coordinate in below order, when it is exist on the box
    8 7 6
    1   5
    2 3 4
    """
    x = pos[0]
    y = pos[1]
    if x > 0:
        yield (x - 1, y)
    if x > 0 and y + 1 < BOARD_SIZE:
        yield (x - 1, y + 1)
    if y + 1 < BOARD_SIZE:
        yield (x, y + 1)
    if x + 1 < BOARD_SIZE and y + 1 < BOARD_SIZE:
        yield (x + 1, y + 1)
    if x + 1 < BOARD_SIZE:
        yield (x + 1, y)
    if x + 1 < BOARD_SIZE and y > 0:
        yield (x + 1, y - 1)
    if y > 0:
        yield (x, y - 1)
    if x > 0 and y > 0:
        yield (x - 1, y - 1)


def swap_tiles(board: List[List[str]], pos1: Tuple[int, int], pos2: Tuple[int, int]):
    tmp = board[pos1[0]][pos1[1]]
    board[pos1[0]][pos1[1]] = board[pos2[0]][pos2[1]]
    board[pos2[0]][pos2[1]] = tmp


def press_red_tile(board: List[List[str]], pos: Tuple[int, int]):
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x][y] == TILE_BLACK:
                board[x][y] = TILE_RED
            elif board[x][y] == TILE_WHITE:
                board[x][y] = TILE_BLACK


def press_black_tile(board: List[List[str]], pos: Tuple[int, int]):
    tmp = board[BOARD_SIZE - 1][pos[1]]
    x = BOARD_SIZE - 1
    while x > 0:
        board[x][pos[1]] = board[x - 1][pos[1]]
        x -= 1
    board[0][pos[1]] = tmp


def press_white_tile(board: List[List[str]], pos: Tuple[int, int]):
    me = board[pos[0]][pos[1]]
    for x in range(max(0, pos[0] - 1), min(BOARD_SIZE, pos[0] + 2)):
        for y in range(max(0, pos[1] - 1), min(BOARD_SIZE, pos[1] + 2)):
            if x != pos[0] and y != pos[1]:
                continue
            if board[x][y] == me:
                board[x][y] = TILE_GREY
            elif board[x][y] == TILE_GREY:
                board[x][y] = me


def press_green_tile(board: List[List[str]], pos: Tuple[int, int]):
    if pos != (int(BOARD_SIZE / 2), int(BOARD_SIZE / 2)):
        swap_tiles(board, pos, (BOARD_SIZE - pos[0] - 1, BOARD_SIZE - pos[1] - 1))


def press_orange_tile(board: List[List[str]], pos: Tuple[int, int]):
    count = {}

    for x, y in surrounding(pos):
        if x != pos[0] and y != pos[1]:
            continue
        tile = board[x][y]
        if tile in count:
            count[tile] = count[tile] + 1
        else:
            count[tile] = 1
    max_color = None
    two_max = False
    for key, value in count.items():
        if value >= 2 and (max_color == None or value > count[max_color]):
            two_max = False
            max_color = key
        elif max_color != None and value == count[max_color]:
            two_max = True

    if max_color != None and two_max == False:
        board[pos[0]][pos[1]] = max_color


def press_violet_tile(board: List[List[str]], pos: Tuple[int, int]):
    if pos[1] + 1 == BOARD_SIZE:
        return

    swap_tiles(board, pos, (pos[0], pos[1] + 1))


def press_yellow_tile(board: List[List[str]], pos: Tuple[int, int]):
    if pos[1] == 0:
        return

    swap_tiles(board, pos, (pos[0], pos[1] - 1))


def press_pink_tile(board: List[List[str]], pos: Tuple[int, int]):
    surroundings = surrounding(pos)
    prev = next(surroundings)
    tmp = board[prev[0]][prev[1]]

    while True:
        next_pos = next(surroundings, None)
        if next_pos == None:
            break
        board[prev[0]][prev[1]] = board[next_pos[0]][next_pos[1]]
        prev = next_pos

    board[prev[0]][prev[1]] = tmp


def press_blue_tile(board: List[List[str]], pos: Tuple[int, int]):
    center_tile = board[int(BOARD_SIZE / 2)][int(BOARD_SIZE / 2)]

    if center_tile == TILE_RED:
        press_red_tile(board, pos)
    elif center_tile == TILE_BLACK:
        press_black_tile(board, pos)
    elif center_tile == TILE_WHITE:
        press_white_tile(board, pos)
    elif center_tile == TILE_GREEN:
        press_green_tile(board, pos)
    elif center_tile == TILE_ORANGE:
        press_orange_tile(board, pos)
    elif center_tile == TILE_VIOLET:
        press_violet_tile(board, pos)
    elif center_tile == TILE_YELLOW:
        press_yellow_tile(board, pos)
    elif center_tile == TILE_PINK:
        press_pink_tile(board, pos)


def press_tile(board: List[List[str]], pos: Tuple[int, int]):
    tile = board[pos[0]][pos[1]]

    if tile == TILE_RED:
        press_red_tile(board, pos)
    elif tile == TILE_BLACK:
        press_black_tile(board, pos)
    elif tile == TILE_WHITE:
        press_white_tile(board, pos)
    elif tile == TILE_GREEN:
        press_green_tile(board, pos)
    elif tile == TILE_ORANGE:
        press_orange_tile(board, pos)
    elif tile == TILE_VIOLET:
        press_violet_tile(board, pos)
    elif tile == TILE_YELLOW:
        press_yellow_tile(board, pos)
    elif tile == TILE_PINK:
        press_pink_tile(board, pos)
    elif tile == TILE_BLUE:
        press_blue_tile(board, pos)


def is_success(board: List[List[str]], corners: List[str]) -> bool:
    return (
        board[0][0] == corners[0]
        and board[BOARD_SIZE - 1][0] == corners[1]
        and board[0][BOARD_SIZE - 1] == corners[2]
        and board[BOARD_SIZE - 1][BOARD_SIZE - 1] == corners[3]
    )


COLOR_BLACK = "\033[30m"
COLOR_RED = "\033[31m"
COLOR_BRIGHT_RED = "\033[91m"
COLOR_GREEN = "\033[32m"
COLOR_YELLOW = "\033[33m"
COLOR_BRIGHT_YELLOW = "\033[93m"
COLOR_BLUE = "\033[34m"
COLOR_MAGENTA = "\033[35m"
COLOR_CYAN = "\033[36m"
COLOR_WHITE = "\033[37m"
COLOR_GREY = "\033[90m"
COLOR_BRIGHT_WHITE = "\033[97m"
COLOR_DEFAULT = "\033[39m"

# COLOR_BLACK = ""
# COLOR_RED = ""
# COLOR_BRIGHT_RED = ""
# COLOR_GREEN = ""
# COLOR_YELLOW = ""
# COLOR_BRIGHT_YELLOW = ""
# COLOR_BLUE = ""
# COLOR_MAGENTA = ""
# COLOR_CYAN = ""
# COLOR_WHITE = ""
# COLOR_GREY = ""
# COLOR_BRIGHT_WHITE = ""
# COLOR_DEFAULT = ""


def print_board(board: List[List[str]], sel: Tuple[int, int] | None = None):
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            tile = board[x][y]
            if sel != None and sel == (x, y):
                print(COLOR_BRIGHT_RED, end="")
                print("[", end="")
                print(COLOR_DEFAULT, end="")
            else:
                print(" ", end="")

            if tile == TILE_RED:
                print(COLOR_RED, end="")
            elif tile == TILE_ORANGE:
                print(COLOR_YELLOW, end="")
            elif tile == TILE_YELLOW:
                print(COLOR_BRIGHT_YELLOW, end="")
            elif tile == TILE_GREEN:
                print(COLOR_GREEN, end="")
            elif tile == TILE_BLUE:
                print(COLOR_BLUE, end="")
            elif tile == TILE_VIOLET:
                print(COLOR_MAGENTA, end="")
            elif tile == TILE_BLACK:
                print(COLOR_GREY, end="")
            elif tile == TILE_WHITE:
                print(COLOR_BRIGHT_WHITE, end="")
            elif tile == TILE_PINK:
                print(COLOR_BRIGHT_RED, end="")
            print(tile, end="")
            if sel != None and sel == (x, y):
                print(COLOR_BRIGHT_RED, end="")
                print("]", end="")
            else:
                print(" ", end="")
            print(COLOR_DEFAULT, end="")
        print("")


def get_board() -> List[List[str]]:
    print(
        f"Input {BOARD_SIZE} x {BOARD_SIZE} square of characters representing the board"
    )
    print(
        f"{COLOR_GREY}b{COLOR_DEFAULT} for black tile, {COLOR_BLUE}B{COLOR_DEFAULT} for blue tile"
    )
    print(
        f"{COLOR_WHITE}g{COLOR_DEFAULT} for grey tile, {COLOR_GREEN}G{COLOR_DEFAULT} for green tile"
    )

    board = []
    for _ in range(BOARD_SIZE):
        line = input()
        board.append(list(line))

    rotate_board: List[List[str]] = []
    for _ in range(BOARD_SIZE):
        col = []
        for _ in range(BOARD_SIZE):
            col.append("x")
        rotate_board.append(col)

    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            rotate_board[x][y] = board[y][x]

    return rotate_board


def get_corner_colors() -> List[str]:
    print("Input colors of the 4 corners in square. Ex: ")
    print("bb")
    print("bb")

    corner = list(input())
    corner.extend(list(input()))

    return corner


@dataclass
class MapNode:
    state: List[List[str]]
    parent_state: List[List[str]] | None
    steps: int
    pressed: Tuple[int, int] | None


def main():
    board = get_board()
    print()
    corners = get_corner_colors()
    print()

    map: Dict[str, MapNode] = {}
    process_queue: List[MapNode] = []
    root_node = MapNode(board.copy(), None, 0, None)
    process_queue.append(root_node)
    map[repr(board)] = root_node

    pass_node = None

    while len(process_queue) > 0:
        node = process_queue.pop(0)
        # print(f"Step {node.steps}")
        # if node.parent_state != None:
        #     print(f"Parent: ")
        #     print_board(node.parent_state, sel=node.pressed)
        #     print()
        # print("Current:")
        # print_board(node.state)
        # print()

        if is_success(node.state, corners):
            pass_node = node
            break
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                new_board = deepcopy(node.state)

                press_tile(new_board, (x, y))
                if repr(new_board) in map:
                    continue

                new_node = MapNode(new_board, node.state, node.steps + 1, (x, y))
                map[repr(new_board)] = new_node
                process_queue.append(new_node)

    if pass_node == None:
        print("Failed to find a solution")
        return

    step_list: List[MapNode] = [pass_node]
    pressed_list: List[Tuple[int, int]] = []
    if pass_node.pressed != None:
        pressed_list.append(pass_node.pressed)

    while True:
        last = step_list[-1]
        if last.parent_state == None:
            break
        node = map[repr(last.parent_state)]
        if node.pressed != None:
            pressed_list.append(node.pressed)
        step_list.append(node)
    step_list.reverse()
    pressed_list.reverse()

    for step in step_list:
        if step.steps < len(pressed_list):
            pressing = pressed_list[step.steps]
            print(f"Step {step.steps}: Press ({pressing[0]}, {pressing[1]}):")
        else:
            print("Finished")
            pressing = None

        if pressing != None:
            print_board(step.state, sel=pressing)
        else:
            print_board(step.state)
        print()


if __name__ == "__main__":
    main()
