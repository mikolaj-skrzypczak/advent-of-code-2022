from utils.utils import load_input


def main() -> None:
    _input = load_input(day=4)
    result_part_one = result_part_two = 0

    for line in _input:
        first, second = line.split(",")
        first = set(range(int(first.split("-")[0]), int(first.split("-")[1]) + 1))
        second = set(range(int(second.split("-")[0]), int(second.split("-")[1]) + 1))

        shorter_len = min(len(first), len(second))
        intersection = first.intersection(second)

        result_part_one += 1 if shorter_len == len(intersection) else 0
        result_part_two += 1 if intersection else 0

    print(f"Part one: {result_part_one}")
    print(f"Part two: {result_part_two}")


if __name__ == '__main__':
    main()
