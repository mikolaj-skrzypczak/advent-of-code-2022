import string

from utils.utils import load_input

vertices_numbers: list[list[int]]

starting_point = 'S'
destination_point = 'E'
letter_to_height_map = {
    letter: height for letter, height in zip(string.ascii_lowercase, range(0, len(string.ascii_lowercase)))} | {
    starting_point: 0,
    destination_point: len(string.ascii_lowercase) - 1
}


def main() -> None:
    _input = load_input(day=12)

    global vertices_numbers
    vertices_numbers = create_vertex_numbers_matrix(_input)
    adjacency_list = create_adjacency_list(_input)

    part_one(_input, adjacency_list)
    part_two(_input, adjacency_list)


def part_one(height_map: list[str], adjacency_list: list[list[int]]) -> None:
    _starting_point = _get_vertex_number(height_map, starting_point)
    _destination_point = _get_vertex_number(height_map, destination_point)
    print(f"Part one: {get_shortest_distance(adjacency_list, _starting_point, _destination_point)}")


def part_two(height_map: list[str], adjacency_list: list[list[int]]) -> None:
    _destination_point = _get_vertex_number(height_map, destination_point)
    distances = [
        get_shortest_distance(adjacency_list, vertices_numbers[i][j], _destination_point)
        for i in range(len(height_map))
        for j in range(len(height_map[i]))
        if (height_map[i][j] == 'a' or height_map[i][j] == 'S')
    ]
    print(f"Part two: {min(distances)}")


def create_vertex_numbers_matrix(height_map: list[str]) -> list[list[int]]:
    def divide_into_chunks(_list, _chunk_size):
        for i in range(0, len(_list), _chunk_size):
            yield _list[i:i + _chunk_size]

    return list(divide_into_chunks([i for i in range(len(height_map) * len(height_map[0]))], len(height_map[0])))


def create_adjacency_list(height_map: list[str]) -> list[list[int]]:
    adjacency_list = [[] for _ in range(vertices_numbers[-1][-1] + 1)]
    for i in range(len(height_map)):
        for j in range(len(height_map[i])):
            adjacency_list[vertices_numbers[i][j]] = _get_all_neighbours(height_map, i, j)
    return adjacency_list


def get_shortest_distance(adjacency_list: list[list[int]], start_vertex_no: int, destination_vertex_no: int) -> int:
    """
    @source: https://www.geeksforgeeks.org/shortest-path-unweighted-graph/
    @author: rutvik_56
    I only refactored names of variables, added typehints and refactored to meet pep8 standards.
    """
    vertices_no = len(adjacency_list)

    predecessors = [0 for _ in range(vertices_no)]
    distances = [0 for _ in range(vertices_no)]

    if not bfs(adjacency_list, start_vertex_no, destination_vertex_no, vertices_no, predecessors, distances):
        pass

    path = []
    crawl = destination_vertex_no
    path.append(crawl)

    while predecessors[crawl] != -1:
        path.append(predecessors[crawl])
        crawl = predecessors[crawl]

    return distances[destination_vertex_no]


def bfs(
        adjacency_list: list[list[int]], start_vertex_no: int, destination_vertex_no: int,
        vertices_no: int, predecessors: list[int], distances: list[int]
) -> bool:
    """
    @source: https://www.geeksforgeeks.org/shortest-path-unweighted-graph/
    @author: rutvik_56
    I only refactored names of variables, added typehints and refactored to meet pep8 standards.
    """
    queue = []
    visited = [False for _ in range(vertices_no)]

    for i in range(vertices_no):
        distances[i] = 1000000
        predecessors[i] = -1

    visited[start_vertex_no] = True
    distances[start_vertex_no] = 0
    queue.append(start_vertex_no)

    while len(queue) != 0:
        u = queue[0]
        queue.pop(0)
        for i in range(len(adjacency_list[u])):

            if not visited[adjacency_list[u][i]]:
                visited[adjacency_list[u][i]] = True
                distances[adjacency_list[u][i]] = distances[u] + 1
                predecessors[adjacency_list[u][i]] = u
                queue.append(adjacency_list[u][i])

                if adjacency_list[u][i] == destination_vertex_no:
                    return True

    return False


def _get_all_neighbours(height_map: list[str], i: int, j: int) -> list[int]:
    def _is_out_of_range(_x, _y):
        return _x < 0 or _y < 0 or _x >= len(height_map) or _y >= len(height_map[i])

    neighbours = []
    current_vertex_height = letter_to_height_map[height_map[i][j]]

    for x, y in zip((1, -1, 0, 0), (0, 0, 1, -1)):
        neighbour_x, neighbour_y = i + x, j + y
        if _is_out_of_range(neighbour_x, neighbour_y):
            continue
        neighbour_height = letter_to_height_map[height_map[i + x][j + y]]
        if neighbour_height - current_vertex_height <= 1:
            neighbours.append(vertices_numbers[neighbour_x][neighbour_y])

    return neighbours


def _get_vertex_number(height_map: list[str], point: str) -> int:
    for i in range(len(height_map)):
        for j in range(len(height_map[i])):
            if height_map[i][j] == point:
                return vertices_numbers[i][j]


if __name__ == '__main__':
    main()
