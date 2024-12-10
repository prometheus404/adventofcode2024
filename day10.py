import sys

test_trail = [
    [8, 9, 0, 1, 0, 1, 2, 3],
    [7, 8, 1, 2, 1, 8, 7, 4],
    [8, 7, 4, 3, 0, 9, 6, 5],
    [9, 6, 5, 4, 9, 8, 7, 4],
    [4, 5, 6, 7, 8, 9, 0, 3],
    [3, 2, 0, 1, 9, 0, 1, 2],
    [0, 1, 3, 2, 9, 8, 0, 1],
    [1, 0, 4, 5, 6, 7, 3, 2],
]


def recursive_path_count(trail, x, y):
    result = set()
    # UP
    if y > 0 and trail[y][x] == trail[y - 1][x] - 1:
        result.update(
            {(x, y - 1)}
            if trail[y - 1][x] == 9
            else recursive_path_count(trail, x, y - 1)
        )
    # LEFT
    if x > 0 and trail[y][x] == trail[y][x - 1] - 1:
        result.update(
            {(x - 1, y)}
            if trail[y][x - 1] == 9
            else recursive_path_count(trail, x - 1, y)
        )
    # DOWN
    if y < len(trail) - 1 and trail[y][x] == trail[y + 1][x] - 1:
        result.update(
            {(x, y + 1)}
            if trail[y + 1][x] == 9
            else recursive_path_count(trail, x, y + 1)
        )
    # RIGHT
    if x < len(trail[0]) - 1 and trail[y][x] == trail[y][x + 1] - 1:
        result.update(
            {(x + 1, y)}
            if trail[y][x + 1] == 9
            else recursive_path_count(trail, x + 1, y)
        )
    return result


def total_path_count(trail):
    # return recursive_pat_count(test_trail, 0, 4)
    return sum(
        [
            len(recursive_path_count(trail, x, y))
            for x in range(len(trail[0]))
            for y in range(len(trail))
            if trail[y][x] == 0
        ]
    )


def revised_path_count(trail, x, y):
    result = 0
    # UP
    if y > 0 and trail[y][x] == trail[y - 1][x] - 1:
        result += 1 if trail[y - 1][x] == 9 else revised_path_count(trail, x, y - 1)
    # LEFT
    if x > 0 and trail[y][x] == trail[y][x - 1] - 1:
        result += 1 if trail[y][x - 1] == 9 else revised_path_count(trail, x - 1, y)
    # DOWN
    if y < len(trail) - 1 and trail[y][x] == trail[y + 1][x] - 1:
        result += 1 if trail[y + 1][x] == 9 else revised_path_count(trail, x, y + 1)
    # RIGHT
    if x < len(trail[0]) - 1 and trail[y][x] == trail[y][x + 1] - 1:
        result += 1 if trail[y][x + 1] == 9 else revised_path_count(trail, x + 1, y)

    return result


def alternative_score(trail):
    # return recursive_pat_count(test_trail, 0, 4)
    return sum(
        [
            revised_path_count(trail, x, y)
            for x in range(len(trail[0]))
            for y in range(len(trail))
            if trail[y][x] == 0
        ]
    )


with open("day10_input") as file:
    trail = [[int(x) for x in line[:-1]] for line in file]
# sys.setrecursionlimit(100000000)
print(total_path_count(trail))
print(alternative_score(trail))
