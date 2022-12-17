from functools import cmp_to_key
from itertools import zip_longest
from typing import Union

from utils.utils import load_input


def main() -> None:
    _input = list(map(eval, filter(lambda x: x, load_input(day=13))))
    print("Part one: ", sum([i // 2 + 1 for i in range(0, len(_input), 2)
                             if are_in_right_order(_input[i], _input[i + 1])]))

    divider_packet_1, divider_packet_2 = [[2]], [[6]]
    _input.extend([divider_packet_1, divider_packet_2])
    _input = sorted(_input, key=cmp_to_key(compare))
    print("Part two: ", (_input.index(divider_packet_1) + 1) * (_input.index(divider_packet_2) + 1))


def are_in_right_order(left: Union[list, int], right: Union[list, int]) -> bool:
    return compare(left, right) == -1


def compare(left: Union[list, int], right: Union[list, int]) -> int:
    def if_both_are_integers() -> int:
        return -1 if left < right else 1 if left > right else 0

    def if_both_are_lists() -> int:
        for i_l, i_r in zip_longest(left, right):
            if (_result := compare(i_l, i_r)) != 0:
                return _result
        return 0

    def if_one_is_list_and_one_is_integer() -> int:
        return compare(
            _convert_to_list_if_necessary(left),
            _convert_to_list_if_necessary(right)
        )

    if left is None:
        return -1
    if right is None:
        return 1

    if isinstance(left, int) and isinstance(right, int):
        return if_both_are_integers()
    if isinstance(left, list) and isinstance(right, list):
        return if_both_are_lists()
    return if_one_is_list_and_one_is_integer()


def _convert_to_list_if_necessary(item: Union[list, int]) -> list:
    return [item] if isinstance(item, int) else item


if __name__ == '__main__':
    main()
