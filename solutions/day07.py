from utils.utils import load_input

TOTAL_DISK_SPACE = 70000000
SPACE_NEEDED = 30000000


def main() -> None:
    _input = load_input(day=7)

    directories_tree = create_directories_tree(_input)
    directories_sizes = calculate_directories_sizes(directories_tree)

    total_space_used = max(directories_sizes)

    space_to_free = SPACE_NEEDED - (TOTAL_DISK_SPACE - total_space_used)

    print(f"Part one: {sum(i for i in directories_sizes if i < 100000)}")
    print(f"Part two: {sorted(i for i in directories_sizes if i >= space_to_free)[0]}")


def create_directories_tree(_input: list[str]) -> dict:
    def cd(_to_where: str) -> None:
        nonlocal read_ls_results
        nonlocal current_directory
        read_ls_results = False
        if _to_where == "..":
            current_directory.pop()
        else:
            current_directory.append(_to_where)

    def get_parent_directory() -> dict:
        nonlocal nested_directories
        nonlocal current_directory
        _parent_directory = nested_directories.get(current_directory[0])
        for directory in current_directory[1:]:
            _parent_directory = _parent_directory.get(directory)
        return _parent_directory

    nested_directories = {"/": {}}
    current_directory = ["/"]

    read_ls_results = False
    for line in _input[1:]:
        if line.startswith("$ cd"):
            cd(line.split()[-1])

        if read_ls_results:
            parent_directory = get_parent_directory()
            if line.startswith("dir"):
                if not parent_directory.get(line.split()[1]):
                    parent_directory[line.split()[1]] = {}
            else:
                size, filename = int(line.split()[0]), line.split()[1]
                parent_directory["f_" + filename] = size

        if line.startswith("$ ls"):
            read_ls_results = True

    return nested_directories


def calculate_directories_sizes(nested_directories: dict, prefix: str = '', result: list = None) -> list[int]:
    if result is None:
        result = []

    for key, value in nested_directories.items():
        if isinstance(value, dict):
            calculate_directories_sizes(value, prefix + key + '/', result)
            result.append(_get_recursive_size(value))

    return result


def _get_recursive_size(directory: dict) -> int:
    size = 0
    for key, value in directory.items():
        if key.startswith("f_"):
            size += value
        else:
            size += _get_recursive_size(value)
    return size


if __name__ == '__main__':
    main()
