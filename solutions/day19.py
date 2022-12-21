import re
from dataclasses import dataclass

import numpy as np
from ortools.sat.python import cp_model

from utils.utils import load_input

"""
When reading the description for day 19 puzzle, it immediately reminded me of linear programming problems
which I used to solve during the 6th semester of my studies. I knew that I could yet again write write some kind of
graph representation of the problem, and use DFS or BFS to find the optimal solution, but after using this 
approach for the previous puzzles, I decided I wanted to learn something knew.

I found an amazing solution for the puzzle by a Reddit user zero_mod_p which uses the Google OR-Tools library.
Instead of writing longish solutions which would eat up a lot of RAM and were time consuming, this solver
from google is able to solve the problem in a matter of seconds.

I WANT TO HIGHLIGHT THAT I DID NOT WRITE THIS SOLUTION. I just added typing and refactored same variables.
Huge shoutout to zero_mod_p for this amazing solution! I loved the opportunity to learn about OR-Tools library.
Here is the link to the original solution:
https://neptyne.com/neptyne/m6z0yosx5n#cs=0&cev=true
"""

COSTS_RE = re.compile(r"Each (ore|clay|obsidian|geode) robot costs ([^.]+)\.")


def main() -> None:
    _input = load_input(day=19)
    print(f"Part one: {sum(i * maximize(blueprint, time=24) for i, blueprint in enumerate(get_blueprints(_input), 1))}")
    print(f"Part two: {np.prod([maximize(blueprint, time=32) for blueprint in get_blueprints(_input)[:3]])}")


@dataclass
class Cost:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0

    def array(self):
        return np.array([self.ore, self.clay, self.obsidian, 0])


@dataclass
class Blueprint:
    ore: Cost
    clay: Cost
    obsidian: Cost
    geode: Cost

    def matrix(self):
        return np.array(
            [
                self.ore.array(),
                self.clay.array(),
                self.obsidian.array(),
                self.geode.array(),
            ]
        ).T


def maximize(blueprint: Blueprint, time: int = 24) -> int:
    model = cp_model.CpModel()
    blueprint_m = blueprint.matrix()

    states = [(np.array([1, 0, 0, 0]), np.array([0, 0, 0, 0]))]  # Initial state of no resources and a single robot

    for minute in range(time):
        robots, inventory = states[-1]
        build = np.array(
            [
                model.NewIntVar(0, 1, f"{resource}-{minute}")
                for resource in ("ore", "clay", "obsidian", "geode")
            ]
        )
        model.Add(sum(build) <= 1)  # We can build only 1 robot per minute
        cost = (blueprint_m * build).sum(axis=1)
        inventory = inventory - cost
        for i in inventory:
            model.Add(i >= 0)
        states.append((robots + build, inventory + robots))

    model.Maximize(states[-1][-1][-1])  # [last state, inventory, geodes]
    solver = cp_model.CpSolver()
    res = solver.Solve(model)
    assert cp_model.OPTIMAL == res, solver.StatusName(res)

    return int(solver.ObjectiveValue())


def get_blueprints(_input: list[str]) -> list[Blueprint]:
    return [Blueprint(**{robot: parse_costs(cost) for robot, cost in COSTS_RE.findall(line)}) for line in _input]


def parse_costs(line: str) -> Cost:
    quantities_and_resource_paired = [quantity_to_resource.split() for quantity_to_resource in line.split(" and ")]
    return Cost(**{resource: int(quantity) for quantity, resource in quantities_and_resource_paired})


if __name__ == '__main__':
    main()
