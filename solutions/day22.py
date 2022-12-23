import re
from functools import reduce

import numpy as np

from utils.utils import load_input

"""
Part one was really fun and I solved without the need of external help.

Part two would have taken me several business days and I found 0 inspiration on the subreddit.
Most solutions included there had some hard-coding based on the given input, which I didn't feel like doing.
With a heavy heart, I decided to shift my focus to other (university related) tasks.

I did however find a mind-blowing one-liner solution by kaa-the-wise (reddit).
I won't even try to encompass it with my mind, but I'm leaving it here (line 155) as a tidbit.
Can't imagine the thought process that went into this one. It is amazing that kaa-the-wise
was able to come up with a one-liner solution for the puzzle that most (python) programmers
need approximately 200 lines of code to solve.
"""

VOID = 0
OPEN_TILE = 1
WALL = 2
CURRENT_DIRECTION = 'RIGHT'
CURRENT_POSITION: tuple[int, int] | None = None
TURN_RIGHT = {
    "RIGHT": "DOWN",
    "DOWN": "LEFT",
    "LEFT": "UP",
    "UP": "RIGHT",
}
TURN_LEFT = {
    "RIGHT": "UP",
    "UP": "LEFT",
    "LEFT": "DOWN",
    "DOWN": "RIGHT",
}
DIRECTION_BONUS = {
    "RIGHT": 0,
    "DOWN": 1,
    "LEFT": 2,
    "UP": 3,
}


def main() -> None:
    _input = load_input(day=22, strip=False)
    board, moves = parse_input(_input)
    do_moves(board, moves)
    print(f"Part one: {1000 * CURRENT_POSITION[0] + 4 * CURRENT_POSITION[1] + DIRECTION_BONUS[CURRENT_DIRECTION]}")
    part_two(_input)


def do_moves(board: np.ndarray, moves: list[int | str]) -> None:
    for move in moves:
        if isinstance(move, int):
            move_forward(board, move)
        else:
            turn(move)


def move_forward(board: np.ndarray, steps: int) -> None:
    global CURRENT_POSITION
    y, x = CURRENT_POSITION
    for _ in range(steps):
        y, x = wrap_around_the_edges(board, take_one_step(y, x))
        if board[y][x] == WALL:
            break
        CURRENT_POSITION = y, x


def take_one_step(y: int, x: int) -> tuple[int, int]:
    match CURRENT_DIRECTION:
        case "RIGHT":
            x += 1
        case "DOWN":
            y += 1
        case "LEFT":
            x -= 1
        case "UP":
            y -= 1
    return y, x


def wrap_around_the_edges(board: np.ndarray, position: tuple[int, int]) -> tuple[int, int]:
    y, x = position
    if board[y][x] == VOID:
        match CURRENT_DIRECTION:
            case "RIGHT":
                x = 0
            case "DOWN":
                y = 0
            case "LEFT":
                x = board.shape[1] - 1
            case "UP":
                y = board.shape[0] - 1

        while board[y][x] == VOID:
            y, x = take_one_step(y, x)

    return y, x


def turn(direction: str) -> None:
    global CURRENT_DIRECTION
    match direction:
        case "L":
            CURRENT_DIRECTION = TURN_LEFT[CURRENT_DIRECTION]
        case "R":
            CURRENT_DIRECTION = TURN_RIGHT[CURRENT_DIRECTION]


def parse_input(_input: list[str]) -> tuple[np.ndarray, list[int | str]]:
    board_end_index = _input.index("\n")
    raw_board_lines = _input[:board_end_index]
    instructions = _input[board_end_index + 1]
    return create_board(raw_board_lines), parse_instructions(instructions)


def create_board(raw_board_lines: list[str]) -> np.ndarray:
    def _rstrip(_line: str) -> str:
        return _line.rstrip()

    global CURRENT_POSITION

    board_lines = list(map(_rstrip, raw_board_lines))
    height = len(board_lines)
    width = len(max(board_lines, key=len))

    board = np.zeros((height, width), dtype=int)
    for y, line in enumerate(board_lines):
        for x, char in enumerate(line):
            if char == "#":
                board[y, x] = WALL
            elif char == ".":
                if not CURRENT_POSITION:
                    CURRENT_POSITION = (y, x)
                board[y, x] = OPEN_TILE

    # surround board with void for easier conditionals later
    # this allows to only check for void rather than bounds and void
    additional_void_col = np.zeros((height, 1), dtype=int)
    additional_void_row = np.zeros((1, width + 2), dtype=int)
    board = np.c_[additional_void_col, board, additional_void_col]
    board = np.r_[additional_void_row, board, additional_void_row]
    # correction for current position due to additional void rows and cols
    CURRENT_POSITION = (CURRENT_POSITION[0] + 1, CURRENT_POSITION[1] + 1)
    return board


def parse_instructions(instructions: str) -> list[int | str]:
    return [int(x) if x.isdigit() else x for x in re.findall(r"\d+|L|R", instructions)]


def part_two(_input: list[str]) -> None:
    """
    @author: kaathewise (github username)
    @source: https://github.com/kaathewise/aoc2022/blob/main/22.py
    """
    (S := _input) \
        and (
            m := {
                i + 1j * j: (c == '.')
                for i, s in enumerate(S[:-2])
                for j, c in enumerate(s.rstrip())
                if c in '.#'
            }) \
        and (g := {}) \
        or (n := lambda x, d: [(x, -d * 1j), (x - d * 1j, d), (x + d * (1 - 1j), d * 1j)][c(x, d)]) \
        and (c := lambda x, d: len({x - d * 1j, x - d * 1j + d} & m.keys())) \
        and (
            f := lambda x: (
                y := c(*x) == 2
                and n(*x)
                or (z := f(n(*x)))
                and (z[0] + c(*x) and z[1] or f(z[1])[1])
            ) and g.update({x: (y[0], -y[1]), y: (x[0], -x[1])}) or (c(*y), n(*y))) \
        and f(
            next((x, d) for x in m for d in [1, -1, 1j, -1j]
                 if x + d not in m and x + d * (1 + 1j) in m)) \
        and (j := lambda x, d: g.get((x, d), (x + d, d))) \
        and (x := reduce(
            lambda x, p: (x[0], x[1] * 1j * (1 - 2 * (p == 'R')))
            if p in 'RL' else reduce(lambda y, _: j(*y) if m[j(*y)[0]] else y, range(int(p)), x),
            re.findall(r'\d+|R|L', S[-1]), (min(m, key=lambda x: (x.real, x.imag)), 1j))) \
        and print(f"Part two: {1000 * x[0].real + 4 * x[0].imag + 1004 + [1j, 1, -1j, -1].index(x[1]):.0f}")


if __name__ == '__main__':
    main()
