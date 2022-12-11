def read_file(filename: str) -> list[str]:
    with open(filename, "r") as fp:
        return fp.readlines()


def load_input(day: int, strip: bool = True) -> list[str]:
    with open(f"../inputs/day{day:02d}.txt", "r") as fp:
        return [line.strip() if strip else line for line in fp.readlines()]
