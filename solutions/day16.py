from utils.utils import load_input
from collections import deque, defaultdict
import re

flow_rates = {}
neighbours = {}

"""
Unfortunately, I found this puzzle too challenging to solve in a reasonable time.
After several hours of trying to find a solution, I decided to look for a Python solution on the subreddit.
I came across a video by Sourish Sharma. In the video you can go through the whole coding process.
At the end the author explains the whole idea of the solution.
The code you can see below is basically a copy of the code from the video, with variable
names refactored to user-friendly ones with some minor changes.
The main issue of the solution is that the RAM consumption is enormous.
Unfortunately, it is unable to find the solution for the second part of the puzzle with the input which I got.
Nevertheless, I decided to leave the code here, because the video helped me to understand the problem.
I hope that one day I will be able to solve this puzzle on my own.
Here is the link to the video: https://www.youtube.com/watch?v=FDbqq1wawcY&ab_channel=SourishSharma

PS:
Here is another solution which I found incredibly interesting (and it's really fast):
https://www.reddit.com/r/adventofcode/comments/zn6k1l/comment/j0juwj4/?utm_source=share&utm_medium=web2x&context=3
"""


def main() -> None:
    parse_input(load_input(day=16))
    print(f"Part one: {part_one()}")
    part_two()


def parse_input(_input: list[str]) -> None:
    for line in _input:
        valve, flow_rate = re.match(r'Valve (.*) has flow rate=(\d+)', line).groups()
        valve_neighbours = re.search('tunnels? leads? to valves? (.*)$', line).group(1).replace(" ", "").split(',')

        flow_rates[valve] = int(flow_rate)
        neighbours[valve] = valve_neighbours


def part_one() -> int:
    _queue = deque([(0, (), "AA", 0)])
    visited = set()
    released = 0

    while _queue:
        minute, opened, current, total = _queue.popleft()
        if minute == 30:
            released = max(released, total)
            continue
        if (opened, current) in visited:
            continue
        visited.add((opened, current))

        _total = total
        for valve in opened:
            _total += flow_rates[valve]
        if flow_rates[current] > 0:
            if current not in opened:
                _queue.append((minute + 1, tuple(list(opened) + [current]), current, _total))

        for neighbour in neighbours[current]:
            _queue.append((minute + 1, opened, neighbour, _total))

    return released


def part_two() -> int:
    _queue = deque([(0, (), "AA", "AA", 0)])
    visited = set()
    released = 0

    useful_vales_count = len(list(filter(lambda x: x > 0, flow_rates.values())))
    flow_rate_if_all_valves_are_open = sum(flow_rates.values())
    max_at_minute = defaultdict(int)

    while _queue:
        minute, opened, current_human, current_elephant, total = _queue.popleft()
        if minute == 26:
            released = max(released, total)
            print(released)
            continue

        if len(opened) == useful_vales_count:
            released = max(released, (26 - minute) * flow_rate_if_all_valves_are_open + total)
            print(released)
            continue

        if (opened, current_human, current_elephant) in visited or (opened, current_elephant, current_human) in visited:
            continue

        visited.add((opened, current_human, current_elephant))
        visited.add((opened, current_elephant, current_human))

        if minute > 10:
            if total < 8.5 * (max_at_minute[minute] // 10):
                continue

        _total = total
        for i in opened:
            _total += flow_rates[i]

        max_at_minute[minute] = max(max_at_minute[minute], total)
        if flow_rates[current_human] != 0:

            if current_human not in opened:
                human_opened = tuple(list(opened) + [current_human])

                if flow_rates[current_elephant] != 0:
                    if current_elephant not in opened and current_elephant != current_human:
                        both_opened = tuple(list(human_opened) + [current_elephant])
                        _queue.append((minute + 1, both_opened, current_human, current_elephant, _total))

                        if current_elephant != "AA":
                            continue

                for i in neighbours[current_elephant]:
                    _queue.append((minute + 1, human_opened, current_human, i, _total))

        if flow_rates[current_elephant] != 0:
            if current_elephant not in opened:
                human_opened = tuple(list(opened) + [current_elephant])

                for i in neighbours[current_human]:
                    if i in opened:
                        continue
                    _queue.append((minute + 1, human_opened, i, current_elephant, _total))

                if current_elephant != "AA":
                    continue

        for i in neighbours[current_human]:
            for ii in neighbours[current_elephant]:
                _queue.append((minute + 1, opened, i, ii, _total))


if __name__ == '__main__':
    main()
