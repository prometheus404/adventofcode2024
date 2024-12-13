test_map = [
    ["R", "R", "R", "R", "I", "I", "C", "C", "F", "F"],
    ["R", "R", "R", "R", "I", "I", "C", "C", "C", "F"],
    ["V", "V", "R", "R", "R", "C", "C", "F", "F", "F"],
    ["V", "V", "R", "C", "C", "C", "J", "F", "F", "F"],
    ["V", "V", "V", "V", "C", "J", "J", "C", "F", "E"],
    ["V", "V", "I", "V", "C", "C", "J", "J", "E", "E"],
    ["V", "V", "I", "I", "I", "C", "J", "J", "E", "E"],
    ["M", "I", "I", "I", "I", "I", "J", "J", "E", "E"],
    ["M", "I", "I", "I", "S", "I", "J", "E", "E", "E"],
    ["M", "M", "M", "I", "S", "S", "J", "E", "E", "E"],
]

test_map = [
    ["E", "E", "E", "E", "E"],
    ["E", "X", "X", "X", "X"],
    ["E", "E", "E", "E", "E"],
    ["E", "X", "X", "X", "X"],
    ["E", "E", "E", "E", "E"],
]

test_map = [
    ["A", "A", "A", "A", "A", "A"],
    ["A", "A", "A", "B", "B", "A"],
    ["A", "A", "A", "B", "B", "A"],
    ["A", "B", "B", "A", "A", "A"],
    ["A", "B", "B", "A", "A", "A"],
    ["A", "A", "A", "A", "A", "A"],
]

# notice how the next direction is a 90deg turn clockwise, this is important in get_discounted
directions = [
    (-1, 0),  # left
    (0, 1),  # down
    (1, 0),  # right
    (0, -1),  # up
]


def legal(pos):
    return (0 <= pos[0] < max_x) and (0 <= pos[1] < max_y)


def get_perimeter(region):
    acc = 0
    for r in region:
        for d in directions:
            nxt = (r[0] + d[0], r[1] + d[1])
            acc += (not legal(nxt) and 1) or (0 if nxt in region else 1)
    return acc


def move(p, d):
    return (p[0] + d[0], p[1] + d[1])


# change direction (clockwise by default)
def turn(d, cclock=False):
    if cclock:
        return directions[(directions.index(d) + 1) % len(directions)]
    else:
        return directions[(directions.index(d) - 1) % len(directions)]


def find_all_borders(region):
    return {(p, d) for p in region for d in directions if move(p, d) not in region}


def find_corners(region):
    acc = 0
    # check corner made by a single plot
    borders = find_all_borders(region)
    for p, d in list(borders):
        if (p, turn(d)) in borders and move(move(p, turn(d)), d) not in region:
            acc += 1
            borders.discard((p, d))
        if (p, turn(d, cclock=True)) in borders and (
            move(move(p, turn(d, cclock=True)), d) not in region
        ):
            acc += 1
            borders.discard((p, d))
    # check corners made by two plot
    borders = find_all_borders(region)
    for p, d in list(borders):
        for p2, d2 in list(borders):
            if (
                move(p, d) == move(p2, d2)
                and abs(p[0] - p2[0]) == 1
                and abs(p[1] - p2[1]) == 1
            ):  # the second check is necessary to avoid ABA cases
                acc += 1
                borders.discard((p, d))
    return acc


def get_area(region):
    return len(region)


def get_nearby(p, garden, plot, acc=set(), remaining=set()):
    if len(acc) == 0:
        acc = {p}
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    nearby = {
        (plot.remove((p2[0], p2[1])) or (p2[0], p2[1]))
        for d in directions
        if (
            ((p2 := (p[0] + d[0], p[1] + d[1])) in plot)
            and (garden[p[0]][p[1]] == garden[p2[0]][p2[1]])
        )
    }
    remaining.update(nearby)
    acc.update(nearby)
    return (
        acc
        if len(remaining) == 0
        else get_nearby(remaining.pop(), garden, plot, acc, remaining)
    )


def get_regions(garden):
    max_x = len(garden)
    max_y = len(garden[0])
    plot = {(i, j) for i in range(max_x) for j in range(max_y)}
    regions = []
    while len(plot) > 0:
        p = plot.pop()
        n = get_nearby(p, garden, plot, acc=set(), remaining=set())
        regions.append(n)
    return regions


with open("day12_input") as file:
    garden_map = [[x for x in line[:-1]] for line in file]
# garden_map = test_map
max_x = len(garden_map)
max_y = len(garden_map[0])
print(sum([get_area(r) * get_perimeter(r) for r in get_regions(garden_map)]))
# [print("region:", r, "fences:", find_corners(r)) for r in get_regions(garden_map)]
print(sum([find_corners(r) * get_area(r) for r in get_regions(garden_map)]))
