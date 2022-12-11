from math import prod

from utils.utils import load_input

forest = []
all_directions = ['up', 'down', 'left', 'right']


def main() -> None:
    _input = load_input(day=8)

    global forest
    forest = prepare_forest_matrix(_input)

    print(f"Part one: {sum([1 if is_visible(i, j) else 0 for i in range(len(forest)) for j in range(len(forest[i]))])}")
    print(f"Part two: {max([get_scenic_score(i, j) for i in range(len(forest)) for j in range(len(forest[i]))])}")


def prepare_forest_matrix(_input: list[str]) -> list[list[int]]:
    return [[int(tree_height) for tree_height in line] for line in _input]


def is_visible(x: int, y: int) -> bool:
    if any([is_visible_from(x, y, direction) for direction in all_directions]):
        return True
    return False


def get_scenic_score(x: int, y: int) -> int:
    return prod(look_in_direction(x, y, direction) for direction in all_directions)


def is_visible_from(x: int, y: int, direction: str) -> bool:
    def determine_start_stop_step_and_iteration_directions() -> tuple[int, int, int, bool, bool]:
        match direction:
            case 'up':
                return 0, x, 1, True, False
            case 'down':
                return len(forest) - 1, x, -1, True, False
            case 'left':
                return 0, y, 1, False, True
            case 'right':
                return len(forest[x]) - 1, y, -1, False, True

    range_start, range_stop, step, should_iterate_over_rows, should_iterate_over_columns = \
        determine_start_stop_step_and_iteration_directions()

    for i in range(range_start, range_stop, step):
        if forest[i if should_iterate_over_rows else x][i if should_iterate_over_columns else y] >= forest[x][y]:
            return False
    return True


def look_in_direction(x: int, y: int, direction: str) -> int:
    def determine_start_stop_step_and_iteration_directions() -> tuple[int, int, int, bool, bool]:
        match direction:
            case 'up':
                return x - 1, -1, -1, True, False
            case 'down':
                return x + 1, len(forest), 1, True, False
            case 'left':
                return y - 1, -1, -1, False, True
            case 'right':
                return y + 1, len(forest[x]), 1, False, True

    own_height = forest[x][y]
    visible_trees = 0

    range_start, range_stop, step, should_iterate_over_rows, should_iterate_over_columns = \
        determine_start_stop_step_and_iteration_directions()

    for i in range(range_start, range_stop, step):
        visible_trees += 1
        if forest[i if should_iterate_over_rows else x][i if should_iterate_over_columns else y] >= own_height:
            break

    return visible_trees


if __name__ == '__main__':
    main()
