from utils.utils import load_input

SNAFU_TO_DEC = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2,
}

DEC_TO_SNAFU = {
    0: '0',
    1: '1',
    2: '2',
    3: '=',
    4: '-',
}


def main() -> None:
    _input = load_input(day=25)
    _sum = 0
    for number in _input:
        _sum += snafu_to_dec(number)
    print(f"Part one: {dec_to_snafu(_sum)}")


def snafu_to_dec(snafu_number: str) -> int:
    dec = 0
    for i, char in enumerate(reversed(snafu_number)):
        dec += SNAFU_TO_DEC[char] * 5 ** i
    return dec


def dec_to_snafu(dec_number: int) -> str:
    snafu = ''
    while dec_number:
        dec_number, reminder = divmod(dec_number, 5)
        snafu = DEC_TO_SNAFU[reminder] + snafu
        if reminder in (3, 4):
            dec_number += 1
    return snafu


if __name__ == '__main__':
    main()
