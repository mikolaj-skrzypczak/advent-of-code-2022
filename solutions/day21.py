import re
from dataclasses import dataclass
from typing import Union

from utils.utils import load_input

BINARY_SEARCH_LOWER_BOUND = - 0
BINARY_SEARCH_UPPER_BOUND = 10 ** 16


@dataclass
class Expression:
    left: str
    right: str
    operator: str


def main() -> None:
    monkeys = prepare_monkeys(load_input(day=21))
    print(f"Part one: {int(find_value(monkey_name='root', monkeys=monkeys))}")
    set_proper_humn_value(monkeys=monkeys)
    print(f"Part two: {monkeys['humn']}")


def find_value(monkey_name: str, monkeys: dict[str, Union[int, Expression]]) -> float:
    if isinstance(monkeys[monkey_name], int):
        return monkeys[monkey_name]

    left = monkeys[monkey_name].left
    right = monkeys[monkey_name].right
    operator = monkeys[monkey_name].operator

    if isinstance(monkeys[left], int) and isinstance(monkeys[right], int):
        return eval(f"{monkeys[left]} {operator} {monkeys[right]}")
    else:
        left = find_value(left, monkeys)
        right = find_value(right, monkeys)
        return eval(f"{left} {operator} {right}")


def set_proper_humn_value(monkeys: dict[str, Union[int, Expression]]) -> None:
    left = find_value(monkeys['root'].left, monkeys)
    right = find_value(monkeys['root'].right, monkeys)
    diff = left - right

    if not int(diff) == 0:
        modify_humn(diff, monkeys)
        set_proper_humn_value(monkeys)


def modify_humn(diff: float, monkeys: dict[str, Union[int, Expression]]) -> None:
    global BINARY_SEARCH_LOWER_BOUND, BINARY_SEARCH_UPPER_BOUND
    current_humn = monkeys['humn']

    new_humn = (BINARY_SEARCH_LOWER_BOUND + BINARY_SEARCH_UPPER_BOUND) // 2
    monkeys['humn'] = new_humn
    if diff < 0:
        BINARY_SEARCH_UPPER_BOUND = current_humn
    else:
        BINARY_SEARCH_LOWER_BOUND = current_humn


def prepare_monkeys(_input: list[str]) -> dict[str, Union[int, Expression]]:
    pattern = re.compile(r'([a-z]+): (?:(\d+)|([a-z]+) ([*/+-]) ([a-z]+))')

    monkeys = {}

    for line in _input:
        monkey, value, left, operator, right = pattern.match(line).groups()

        if value:
            monkeys[monkey] = int(value)
        else:
            monkeys[monkey] = Expression(left, right, operator)

    return monkeys


if __name__ == '__main__':
    main()
