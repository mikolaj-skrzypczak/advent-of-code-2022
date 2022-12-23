import importlib

# choose between 1 and 25
DAY = 22


def main() -> None:
    try:
        solution = importlib.import_module(f"solutions.day{DAY:02d}")
    except ModuleNotFoundError:
        print("Choose a day between 1 and 25!")
        return

    print(
        f"Puzzle description: https://adventofcode.com/2022/day/{DAY}\n"
        f"Answer given input from /inputs/day{DAY:02d}.txt:"
    )
    solution.main()


if __name__ == '__main__':
    main()
