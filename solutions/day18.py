from copy import deepcopy

import fill_voids
import numpy as np

from utils.utils import load_input

"""
The idea of using fill_voids "cheat" in part 2 comes from a reddit user asavar.
It is amazing how much stuff you can do with python libraries.
That is exactly why I love it!
"""


def main() -> None:
    grid = build_grid([tuple(map(int, line.split(","))) for line in load_input(day=18)])
    print("Part one:", calculate_surface_area(grid))
    print("Part two:", calculate_surface_area(grid, fill_air_patches=True))


def build_grid(cube_coords: list[tuple[int, ...]]) -> np.ndarray:
    max_x = max(cube_coords, key=lambda i: i[0])[0]
    max_y = max(cube_coords, key=lambda i: i[1])[1]
    max_z = max(cube_coords, key=lambda i: i[2])[2]

    grid = np.zeros((max_x + 2, max_y + 2, max_z + 2), dtype=int)
    for cube in cube_coords:
        grid[cube[0], cube[1], cube[2]] = 1
    return grid


def calculate_surface_area(grid: np.ndarray, fill_air_patches: bool = False) -> int:
    _grid = deepcopy(grid)
    if fill_air_patches:
        _grid = fill_voids.fill(grid)

    area = 0
    for x in range(_grid.shape[0]):
        for y in range(_grid.shape[1]):
            for z in range(_grid.shape[2]):
                if _grid[x][y][z] == 1:
                    if _grid[x - 1][y][z] == 0:
                        area += 1
                    if _grid[x + 1][y][z] == 0:
                        area += 1
                    if _grid[x][y - 1][z] == 0:
                        area += 1
                    if _grid[x][y + 1][z] == 0:
                        area += 1
                    if _grid[x][y][z - 1] == 0:
                        area += 1
                    if _grid[x][y][z + 1] == 0:
                        area += 1
    return area


if __name__ == '__main__':
    main()
