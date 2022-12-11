import copy
import re

from utils.utils import load_input


def main() -> None:
    _input = load_input(day=5, strip=False)
    instructions_start_index = _input.index('\n') + 1

    n_stacks = int(_input[instructions_start_index - 2].split(" ")[-1])

    stacks_part_one = [[] for _ in range(n_stacks)]
    _fill_stacks(_input[:instructions_start_index - 2], stacks_part_one)
    stacks_part_two = copy.deepcopy(stacks_part_one)

    for instruction in _input[instructions_start_index:]:
        how_many, from_where, to_where = \
            map(int, re.match(r"^move (\d+) from (\d+) to (\d+)$", instruction.strip()).groups())
        _move_boxes(stacks_part_one, from_where - 1, to_where - 1, how_many, reverse=True)
        _move_boxes(stacks_part_two, from_where - 1, to_where - 1, how_many, reverse=False)

    print(f"Part one: {''.join(stack[-1] for stack in stacks_part_one)}")
    print(f"Part two: {''.join(stack[-1] for stack in stacks_part_two)}")


def _fill_stacks(stacks_starting_setup: list[str], stacks: list[list[str]]) -> None:
    for stack_level in reversed(stacks_starting_setup):
        for i, box in enumerate(re.sub("[\\[\\]\\n]", " ", stack_level)):
            stacks[(i - 1) // 4].append(box) if box != ' ' else None


def _move_boxes(
        stacks: list[list[str]],
        from_stack_index: int,
        to_stack_index: int,
        how_many: int,
        reverse: bool = False
) -> None:
    moved_crates = stacks[from_stack_index][-how_many:]
    stacks[from_stack_index] = stacks[from_stack_index][:len(stacks[from_stack_index]) - how_many]
    stacks[to_stack_index].extend(reversed(moved_crates) if reverse else moved_crates)


if __name__ == '__main__':
    main()
