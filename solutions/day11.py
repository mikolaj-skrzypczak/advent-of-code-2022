import copy
import math
from typing import Callable
from sympy import *

from utils.utils import load_input

LCM = 0


def main() -> None:
    clean_input = list(filter(lambda x: x and not x.startswith("Monkey"), load_input(day=11)))
    monkeys = create_monkeys(clean_input)

    global LCM
    LCM = math.lcm(*[monkey.mod for monkey in monkeys])

    print(f"Part one: {solve(monkeys, 20, worry_level=3)}")
    print(f"Part two: {solve(monkeys, 10000, worry_level=0)}")


class Monkey:
    def __init__(
            self, items: list[int], operation: Callable, mod: int,
            to_whom_if_true: int, to_whom_if_false: int, all_monkeys_list: list["Monkey"]
    ):
        x = Symbol('x')
        self.items = items
        self.operation = operation
        self.test = Lambda(x, Eq(x % mod, 0))
        self.to_whom_if_true = to_whom_if_true
        self.to_whom_if_false = to_whom_if_false
        self.inspect_counts = 0
        self.all_monkeys_list = all_monkeys_list
        self.mod = mod

    def inspect_items(self, worry_level) -> None:
        for item in self.items:
            self.inspect_counts += 1

            item = self.operation(item) // worry_level if worry_level else self.operation(item) % LCM

            if self.test(item):
                self.throw_item(item, self.to_whom_if_true)
            else:
                self.throw_item(item, self.to_whom_if_false)

        self.items = []

    def throw_item(self, item: int, to_whom: int) -> None:
        self.all_monkeys_list[to_whom].items.append(item)


def solve(monkeys: list[Monkey], rounds: int, worry_level: int) -> int:
    monkeys = copy.deepcopy(monkeys)

    for i in range(rounds):
        for monkey in monkeys:
            monkey.inspect_items(worry_level=worry_level)

    inspect_counts = sorted(monkey.inspect_counts for monkey in monkeys)
    return inspect_counts[-1] * inspect_counts[-2]


def create_monkeys(clean_input: list[str]) -> list[Monkey]:
    def extract_items() -> list[int]:
        return list(map(int, curr_monkey_lines[0].replace(" ", "").split(":")[1].split(",")))

    def extract_operation() -> Callable:
        operation = curr_monkey_lines[1]
        operator = operation.split(" ")[-2]
        second_number = operation.split(" ")[-1]
        return lambda x: \
            x * (x if second_number == 'old' else int(second_number)) if operator == '*' else \
            x + (x if second_number == 'old' else int(second_number)) if operator == '+' else None

    def extract_test() -> int:
        return int(curr_monkey_lines[2].split(" ")[-1])

    def extract_to_whom_if_true() -> int:
        return int(curr_monkey_lines[3].split(" ")[-1])

    def extract_to_whom_if_false() -> int:
        return int(curr_monkey_lines[4].split(" ")[-1])

    monkeys = []
    for i in range(0, len(clean_input), 5):
        curr_monkey_lines = clean_input[i:i + 5]
        monkeys.append(Monkey(
            extract_items(),
            extract_operation(),
            extract_test(),
            extract_to_whom_if_true(),
            extract_to_whom_if_false(),
            monkeys
        ))
    return monkeys


if __name__ == '__main__':
    main()
