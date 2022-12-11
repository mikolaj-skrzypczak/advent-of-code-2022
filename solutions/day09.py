from utils.utils import load_input


def main() -> None:
    _input = load_input(day=9)

    head = [0, 0]
    tail = [0, 0]
    tail_parts = [[0, 0] for _ in range(9)]

    visited_part_one = {(0, 0)}
    visited_part_two = {(0, 0)}

    for line in _input:
        line = line.split(" ")
        direction, times = line[0], int(line[1])

        for i in range(times):
            move_head(head, direction)
            move_tail(head, tail)
            visited_part_one.add(tuple(tail))

            for j in range(len(tail_parts)):
                move_tail(head if j == 0 else tail_parts[j - 1], tail_parts[j])

                if j == len(tail_parts) - 1:
                    visited_part_two.add(tuple(tail_parts[j]))

    print(f"Part one: {len(visited_part_one)}")
    print(f"Part two: {len(visited_part_two)}")


def move_head(_head: list[int], _direction: str) -> None:
    match _direction:
        case 'U':
            _head[1] += 1
        case 'D':
            _head[1] -= 1
        case 'L':
            _head[0] -= 1
        case 'R':
            _head[0] += 1


def move_tail(_head: list[int], _tail: list[int]) -> None:
    x_dist = _head[0] - _tail[0]
    y_dist = _head[1] - _tail[1]
    if abs(x_dist) > 1 or abs(y_dist) > 1:
        _tail[0] = _tail[0] + (1 if x_dist >= 1 else -1 if x_dist <= -1 else 0)
        _tail[1] = _tail[1] + (1 if y_dist >= 1 else -1 if y_dist <= -1 else 0)


if __name__ == '__main__':
    main()
