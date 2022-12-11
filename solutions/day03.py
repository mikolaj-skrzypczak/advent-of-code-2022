import string

from utils.utils import load_input

WEIGHTS = {letter: weight for letter, weight in zip(string.ascii_letters, range(1, 53))}


def main() -> None:
    _input = load_input(day=3)
    print(f"Part one: {part_one(_input)}")
    print(f"Part two: {part_two(_input)}")


def part_one(_input: list[str]) -> int:
    result = 0
    for line in _input:
        first_backpack, second_backpack = line[:len(line) // 2], line[len(line) // 2:]
        common_char = ''.join(set(first_backpack).intersection(second_backpack))
        result += WEIGHTS[common_char]
    return result


def part_two(_input: list[str]) -> int:
    result = 0
    for i in range(0, len(_input), 3):
        first, second, third = _input[i:i + 3]
        common_char = ''.join(set(first).intersection(second).intersection(third))
        result += WEIGHTS[common_char]
    return result


if __name__ == '__main__':
    main()
