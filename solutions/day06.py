from utils.utils import load_input


def main() -> None:
    stream = load_input(day=6)[0]
    print(f"Part one: {solve(stream, 4)}")
    print(f"Part two: {solve(stream, 14)}")


def solve(stream: str, sequence_length) -> int:
    for i in range(len(stream) - sequence_length):
        if len(set(stream[i:i + sequence_length])) == sequence_length:
            return i + sequence_length


if __name__ == '__main__':
    main()
