from typing import Literal

from utils.utils import load_input

MOVES_TRANSLATION = {
    'A': 'rock',
    'B': 'paper',
    'C': 'scissors',
    'X': 'rock',
    'Y': 'paper',
    'Z': 'scissors'
}

GAME_OUTCOME_TRANSLATIONS = {
    'X': 'lose',
    'Y': 'draw',
    'Z': 'win'
}

POINT_FOR_MOVE = {
    'rock': 1,
    'paper': 2,
    'scissors': 3
}

WHICH_MOVE_TO_CHOOSE_TO_WIN_BASED_ON_OPPONENT_MOVE = {
    'rock': 'paper',
    'paper': 'scissors',
    'scissors': 'rock'
}

WHICH_MOVE_TO_CHOOSE_TO_LOSE_BASED_ON_OPPONENT_MOVE = \
    {value: key for key, value in WHICH_MOVE_TO_CHOOSE_TO_WIN_BASED_ON_OPPONENT_MOVE.items()}


def main() -> None:
    _input = load_input(day=2)
    print(f"Part one: {part_one(_input)}")
    print(f"Part two: {part_two(_input)}")


def part_one(_input: list[str]) -> int:
    result = 0
    for line in _input:
        opponent_move, my_move = list(map(_translate_move, line.split()))
        points_for_game = calculate_game_result(opponent_move, my_move) + POINT_FOR_MOVE[my_move]
        result += points_for_game
    return result


def part_two(_input: list[str]) -> int:
    result = 0

    for line in _input:
        opponent_move, match_result = _translate_move(line.split()[0]), GAME_OUTCOME_TRANSLATIONS[line.split()[1]]

        my_move = chose_my_move_based_on_outcome(opponent_move, match_result)
        points_for_game = calculate_game_result(opponent_move, my_move) + POINT_FOR_MOVE[my_move]
        result += points_for_game

    return result


def calculate_game_result(
        _opponent_move: Literal['rock', 'paper', 'scissors'],
        _my_move: Literal['rock', 'paper', 'scissors']
) -> int:
    if _my_move == _opponent_move:
        return 3
    if (_opponent_move, _my_move) in WHICH_MOVE_TO_CHOOSE_TO_WIN_BASED_ON_OPPONENT_MOVE.items():
        return 6
    return 0


def chose_my_move_based_on_outcome(
        _opponent_move: Literal['rock', 'paper', 'scissors'],
        _match_result: Literal['lose', 'draw', 'win']
) -> Literal['rock', 'paper', 'scissors']:
    match _match_result:
        case 'draw':
            return _opponent_move
        case 'win':
            return WHICH_MOVE_TO_CHOOSE_TO_WIN_BASED_ON_OPPONENT_MOVE[_opponent_move]
        case 'lose':
            return WHICH_MOVE_TO_CHOOSE_TO_LOSE_BASED_ON_OPPONENT_MOVE[_opponent_move]


def _translate_move(move: str) -> Literal['rock', 'paper', 'scissors']:
    return MOVES_TRANSLATION[move]


if __name__ == '__main__':
    main()
