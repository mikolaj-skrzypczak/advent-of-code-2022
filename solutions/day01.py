from utils.utils import load_input


def main() -> None:
    _input = load_input(day=1)

    all_elves_calories = []
    current_elf_sum = 0

    for line in _input:
        if not line:
            all_elves_calories.append(current_elf_sum)
            current_elf_sum = 0
            continue
        current_elf_sum += int(line.strip())

    print(f"Part one: {max(all_elves_calories)}")
    print(f"Part two: {sum(sorted(all_elves_calories)[-3:])}")


if __name__ == '__main__':
    main()
