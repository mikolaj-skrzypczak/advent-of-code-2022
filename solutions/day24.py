from collections import namedtuple, defaultdict, deque

from utils.utils import load_input

ROWS_NUM: int
COLS_NUM: int
BLIZZARD_POSITIONS: defaultdict[int, set[tuple[int, int]]] = defaultdict(set)


def main() -> None:
    global ROWS_NUM, COLS_NUM
    grid = load_input(day=24)
    ROWS_NUM = len(grid)
    COLS_NUM = len(grid[0])
    set_blizzard_positions(grid)
    solve(grid)


def solve(grid: list[str]) -> None:
    State = namedtuple('State', ['row', 'column', 'minute', 'got_end', 'got_start'])

    part_one_printed = False
    seen_states = set()
    initial_state = State(0, 1, 0, False, False)
    _queue = deque([initial_state])

    while _queue:
        row, col, t, got_end, got_start = _queue.popleft()
        if not (0 <= row < ROWS_NUM and 0 <= col < COLS_NUM and grid[row][col] != "#"):
            continue

        if row == ROWS_NUM - 1 and got_end and got_start:
            print(f"Part two: {t}")
            break

        if row == ROWS_NUM - 1:
            got_end = True
            if not part_one_printed:
                part_one_printed = True
                print(f"Part one: {t}")

        if row == 0 and got_end:
            got_start = True

        if (row, col, t, got_end, got_start) in seen_states:
            continue

        seen_states.add((row, col, t, got_end, got_start))

        for x, y in ((0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)):
            if (row + x, col + y) not in BLIZZARD_POSITIONS[t + 1]:
                _queue.append(State(row + x, col + y, t + 1, got_end, got_start))


def set_blizzard_positions(grid: list[str]) -> None:
    global BLIZZARD_POSITIONS
    for t in range(ROWS_NUM * COLS_NUM):
        for row in range(ROWS_NUM):
            for col in range(COLS_NUM):
                match grid[row][col]:
                    case '>':
                        BLIZZARD_POSITIONS[t].add((row, 1 + ((col - 1 + t) % (COLS_NUM - 2))))
                    case '<':
                        BLIZZARD_POSITIONS[t].add((row, 1 + ((col - 1 - t) % (COLS_NUM - 2))))
                    case '^':
                        BLIZZARD_POSITIONS[t].add((1 + ((row - 1 - t) % (ROWS_NUM - 2)), col))
                    case 'v':
                        BLIZZARD_POSITIONS[t].add((1 + ((row - 1 + t) % (ROWS_NUM - 2)), col))


if __name__ == '__main__':
    main()
