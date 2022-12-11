from utils.utils import load_input


def main() -> None:
    _input = load_input(day=10)

    register_states = determine_register_states(_input)

    print(f"Part one: {sum(register_states[i - 1] * i for i in range(20, 221, 40))}")
    print(f"Part two:\n{part_two(register_states)}")  # PLGFKAZG


def determine_register_states(_input: list[str]) -> list[int]:
    register = [1]

    for line in _input:
        if line == "noop":
            register.append(register[-1])
            continue

        register.append(register[-1])
        register.append(register[-1] + int(line.split(" ")[1]))

    return register


def part_two(register_states: list[int]) -> str:
    result = []
    for i in range(1, 241):
        j = (i - 1) % 40
        result.append("#") if abs(register_states[i - 1] - j) <= 1 else result.append(".")

        if i in list(range(40, 241, 40)):
            result.append("\n")

    return "".join(result)


if __name__ == '__main__':
    main()
