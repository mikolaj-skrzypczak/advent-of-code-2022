from utils.utils import load_input

MAX_Y = -float('inf')
SAND_STARTING_POINT = (500, 0)


def main() -> None:
    _input = load_input(day=14)
    all_rocks_corners = get_all_rocks_corners(_input)
    rocks_coords = get_rock_coords(all_rocks_corners)
    update_global_y_max(rocks_coords)
    part_one_result, part_two_result = drop_sand(rocks_coords)
    print(f"Part one result: {part_one_result}")
    print(f"Part two result: {part_two_result}")


def get_all_rocks_corners(_input: list[str]) -> list[list[tuple[int, ...]]]:
    return [[tuple(map(int, corner.strip().split(","))) for corner in line.split("->")] for line in _input]


def get_rock_coords(rocks_corners: list[list[tuple[int, ...]]]) -> set[tuple[int, int]]:
    rock_coords = set()

    for rock_corners in rocks_corners:
        for i in range(len(rock_corners) - 1):
            x1, y1 = rock_corners[i]
            x2, y2 = rock_corners[i + 1]

            xdiff, ydiff = (x2 - x1, y2 - y1)

            iterate_over_x = xdiff != 0
            iterate_over_y = ydiff != 0
            diff = abs(xdiff + ydiff)
            while diff != 0:
                rock_coords.add((x1, y1))
                x1 += (1 if xdiff > 0 else -1) if iterate_over_x else 0
                y1 += (1 if ydiff > 0 else -1) if iterate_over_y else 0
                diff -= 1

            rock_coords.add((x1, y1))

    return rock_coords


def drop_sand(rock_coords: set[tuple[int, int]]) -> tuple[int, int]:
    part_one_result = sand_count = 0

    x, y = SAND_STARTING_POINT
    while True:
        if (x, y) in rock_coords:
            x, y = SAND_STARTING_POINT
        if y > MAX_Y and not part_one_result:
            part_one_result = sand_count

        for _x, _y in [(0, 1), (-1, 1), (1, 1)]:
            if (x + _x, y + _y) not in rock_coords and y < MAX_Y + 1:
                x += _x
                y += _y
                break
        else:
            sand_count += 1
            rock_coords.add((x, y))

        if (x, y) == SAND_STARTING_POINT:
            part_two_result = sand_count
            break

    return part_one_result, part_two_result


def update_global_y_max(rocks_corners: set[tuple[int, int]]) -> None:
    global MAX_Y
    MAX_Y = max([y for _, y in rocks_corners])


if __name__ == '__main__':
    main()
