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


def legal(pos):
    return (0 <= pos[0] < max_x) and (0 <= pos[1] < max_y)


def get_perimeter(region):
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    acc = 0
    for r in region:
        for d in directions:
            nxt = (r[0] + d[0], r[1] + d[1])
            acc += (not legal(nxt) and 1) or (0 if nxt in region else 1)
    return acc


# notice how the next direction is a 90deg turn clockwise, this is important in get_discounted
directions = [
    (-1, 0),  # left
    (0, 1),  # down
    (1, 0),  # right
    (0, -1),  # up
]


def find_border(region):
    for p in region:
        for d in directions:
            if (p[0] + d[0], p[1] + d[1]) not in region:
                return p, d


# change direction (clockwise by default)
def turn(d, cclock=False):
    if cclock:
        return directions[(directions.index(d) + 1) % len(directions)]
    else:
        return directions[(directions.index(d) - 1) % len(directions)]


def move(p, d):
    return (p[0] + d[0], p[1] + d[1])


def get_discounted(region):
    start, border_dir = find_border(region)
    d = turn(border_dir)
    p = start
    acc = 0
    # we follow the border anc count the direction change
    # until we reach the starting point with the same border direction
    while p != start or turn(border_dir) != d or acc == 0:
        # if there is a block in the border direction
        # we change direction counterclockwise and move the point
        border = turn(d, cclock=True)
        if move(p, border) in region:
            d = border
            acc += 1

        p_next = move(p, d)  # next point (only if previous point was in region)
        # check is p_next is inside otherwise change direction
        if p_next not in region:
            d = turn(d)
            acc += 1
            continue
        p = p_next
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
# [print("region:", r, "fences:", get_discounted(r)) for r in get_regions(garden_map)]
print(sum([get_discounted(r) * get_area(r) for r in get_regions(garden_map)]))
