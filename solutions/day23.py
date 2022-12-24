from collections import defaultdict
from copy import deepcopy

from utils.utils import load_input

directions = ['N', 'S', 'W', 'E']
directions_mapping = {
    'N': ((-1, 0), (-1, -1), (-1, 1)),
    'S': ((1, 0), (1, -1), (1, 1)),
    'W': ((0, -1), (-1, -1), (1, -1)),
    'E': ((0, 1), (-1, 1), (1, 1)),
}
potential_neighbour_positions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))


def main() -> None:
    global directions

    elves_positions = get_elves_starting_positions(load_input(day=23))
    rounds_completed = 0

    while True:
        if rounds_completed == 10:
            print(f"Part one: {get_free_tiles_in_smallest_rectangle(elves_positions)}")

        if all_elves_have_no_neighbours(elves_positions):
            print(f"Part two: {rounds_completed + 1}")
            break

        considered_squares = defaultdict(int)
        new_positions = set()
        yet_to_move = set()
        for y, x in elves_positions:
            if has_no_neighbours(y, x, elves_positions) or cant_move(y, x, elves_positions):
                new_positions.add((y, x))
                continue
            for i in range(4):
                tiles_to_check = directions_mapping[directions[i]]
                if tiles_are_taken(y, x, tiles_to_check, elves_positions):
                    continue
                else:
                    dy, dx = tiles_to_check[0]
                    considered_squares[(y + dy, x + dx)] += 1
                    yet_to_move.add((y, x)) if (y, x) not in new_positions else None
                    break

        for y, x in yet_to_move:
            for i in range(4):
                tiles_to_check = directions_mapping[directions[i]]
                if tiles_are_taken(y, x, tiles_to_check, elves_positions):
                    continue
                else:
                    dy, dx = tiles_to_check[0]
                    if considered_squares[(y + dy, x + dx)] == 1:
                        new_positions.add((y + dy, x + dx))
                    else:
                        new_positions.add((y, x))
                    break

        elves_positions = deepcopy(new_positions)
        directions = directions[1:] + [directions[0]]
        rounds_completed += 1


def get_free_tiles_in_smallest_rectangle(elves_positions: set[tuple[int, int]]) -> int:
    return sum(
        1
        for y in range(min(y for y, x in elves_positions), max(y for y, x in elves_positions) + 1)
        for x in range(min(x for y, x in elves_positions), max(x for y, x in elves_positions) + 1)
        if (y, x) not in elves_positions
    )


def get_elves_starting_positions(_input: list[str]) -> set[tuple[int, int]]:
    return set((y, x) for y, line in enumerate(_input) for x, char in enumerate(line) if char == '#')


def tiles_are_taken(
        y: int, x: int,
        tiles_to_check: tuple[tuple[int, int], ...],
        elves_positions: set[tuple[int, int]]
) -> bool:
    return any((y + dy, x + dx) in elves_positions for dy, dx in tiles_to_check)


def all_elves_have_no_neighbours(elves_positions: set[tuple[int, int]]) -> bool:
    return all(has_no_neighbours(y, x, elves_positions) for y, x in elves_positions)


def has_no_neighbours(y: int, x: int, elves_positions: set[tuple[int, int]]) -> bool:
    return all((y + dy, x + dx) not in elves_positions for dy, dx in potential_neighbour_positions)


def cant_move(y: int, x: int, elves_positions: set[tuple[int, int]]) -> bool:
    return all(
        any((y + dy, x + dx) in elves_positions for dy, dx in direction)
        for direction in directions_mapping.values()
    )


if __name__ == '__main__':
    main()
