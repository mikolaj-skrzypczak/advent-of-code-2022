from utils.utils import load_input


def main() -> None:
    encrypted_file = list(map(int, load_input(day=20)))
    print(f"Part one: {solve(encrypted_file)}")
    print(f"Part two: {solve(encrypted_file, decryption_key=811589153, mixin_rounds=10)}")


def solve(encrypted_data: list[int], decryption_key: int = 1, mixin_rounds: int = 1) -> int:
    encrypted_data = [i * decryption_key for i in encrypted_data]
    original_indexes_and_values = [(i, v) for i, v in enumerate(encrypted_data)]

    for _ in range(mixin_rounds):
        for original_index, value in enumerate(encrypted_data):
            moved_index = original_indexes_and_values.index((original_index, value))
            move_to_index = (moved_index + value) % (len(encrypted_data) - 1)
            original_indexes_and_values.insert(move_to_index, original_indexes_and_values.pop(moved_index))

    encrypted = [v for _, v in original_indexes_and_values]
    zero_index = encrypted.index(0)

    return sum([encrypted[(zero_index + i) % len(encrypted)] for i in (1000, 2000, 3000)])


if __name__ == '__main__':
    main()
