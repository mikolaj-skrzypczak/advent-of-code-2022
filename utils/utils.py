import os

inputs_dir = f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/inputs"


def load_input(day: int, strip: bool = True) -> list[str]:
    with open(f"{inputs_dir}/day{day:02d}.txt", "r") as fp:
        return [line.strip() if strip else line for line in fp.readlines()]
