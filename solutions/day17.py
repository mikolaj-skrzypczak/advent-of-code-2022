from utils.utils import load_input

"""
As I found part two incredibly challenging and time-consuming,
it was with pain in my heart that I decided to remove the disgusting attempts to solve it and left only part one.
I found several solutions on the subreddit, including one that particularly caught my attention.
It's incredibly clever (and relatively short). If you'd like to see how part two can be solved, 
I recommend the solution of a github user named corylprince. Link below:
https://github.com/korylprince/adventofcode/blob/master/2022/17/main.py
"""

HORIZONTAL_LINE = ((0, 0), (1, 0), (2, 0), (3, 0))
PLUS_SIGN = ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2))
MIRRORED_L = ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2))
VERTICAL_LINE = ((0, 0), (0, 1), (0, 2), (0, 3))
SQUARE = ((0, 0), (1, 0), (0, 1), (1, 1))

SHAPES = (HORIZONTAL_LINE, PLUS_SIGN, MIRRORED_L, VERTICAL_LINE, SQUARE)
FLOOR = [(x, 0) for x in range(7)]
WINDS_OFFSET = {
    ">": 1,
    "<": -1,
}


def main() -> None:
    winds = load_input(day=17)[0]
    print(f"Part one: {solve(winds, iterations=2022)}")


def solve(winds: str, iterations: int, search_for_cycles: bool = False) -> int:
    tower_height = 0
    occupied_cells = set(FLOOR)
    wind_iterator = 0

    for i in range(iterations):
        rock_coords = get_falling_rock_coords(i, tower_height)
        while True:
            wind_offset = WINDS_OFFSET[winds[wind_iterator % len(winds)]]
            if not would_go_outside_the_walls_or_hit_other(rock_coords, wind_offset, occupied_cells):
                rock_coords = [(x + wind_offset, y) for x, y in rock_coords]

            wind_iterator += 1

            if would_intersect_with_occupied_cells([(x, y - 1) for x, y in rock_coords], occupied_cells):
                break
            else:
                rock_coords = [(x, y - 1) for x, y in rock_coords]

        tower_height = max(tower_height, max(map(lambda _y: _y[1], rock_coords)))
        occupied_cells.update(rock_coords)

        if search_for_cycles:
            pass

    return tower_height


def get_falling_rock_coords(rock_no: int, current_tower_height: int) -> list[tuple[int, int]]:
    chosen_shape = SHAPES[rock_no % len(SHAPES)]
    return [(x + 2, y + 4 + current_tower_height) for x, y in chosen_shape]


def would_go_outside_the_walls_or_hit_other(
        rock_coords: list[tuple[int, int]],
        wind_offset: int,
        occupied_cells: set
) -> bool:
    new_coords = [(x + wind_offset, y) for x, y in rock_coords]
    return any(map(lambda cell: cell[0] < 0 or cell[0] > 6, new_coords)) \
        or would_intersect_with_occupied_cells(new_coords, occupied_cells)


def would_intersect_with_occupied_cells(rock_coords: list[tuple[int, int]], occupied_cells: set) -> bool:
    return any(map(lambda cell: cell in occupied_cells, rock_coords))


if __name__ == '__main__':
    main()
