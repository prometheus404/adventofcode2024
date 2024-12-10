def dist(a, b):
    return abs(a[1] - b[1]) + abs(a[0] - b[0])


def read_antennas(filename):
    dic = {}
    with open(filename) as file:
        y = 0
        for line in file:
            line = line[:-1]  # drop \n
            for x in range(len(line)):
                if line[x] != ".":
                    if line[x] in dic:
                        dic[line[x]] += [(x, y)]
                    else:
                        dic[line[x]] = [(x, y)]
            y += 1
        return (dic, x, y - 1)


# antennas = {"A": [(6, 5), (8, 8), (9, 9)], "0": [(8, 1), (5, 2), (7, 3), (4, 4)]}
# max_y = max_x = 11


def get_antinodes(antennas, max_x, max_y, resonance=False):
    antenna_couples = [
        [(p1, p2) for p1 in antennas[a] for p2 in antennas[a] if p1 != p2]
        for a in antennas
    ]

    results = set()
    for ac in antenna_couples:
        for c in ac:
            p1 = c[0]  # 3,0
            p2 = c[1]  # 2,1
            incr = (p1[0] - p2[0], p1[1] - p2[1])  # (1,-1)

            # increment
            n = 1 - resonance
            while True:
                np = (p1[0] + incr[0] * n, p1[1] + incr[1] * n)
                if 0 <= np[0] <= max_x and 0 <= np[1] <= max_y:
                    n += 1
                    if resonance or dist(np, p1) == 2 * dist(np, p2):
                        results.add(np)

                else:
                    break

            # decrement
            n = 1 - resonance
            while True:
                np = (p1[0] - incr[0] * n, p1[1] - incr[1] * n)
                if 0 <= np[0] <= max_x and 0 <= np[1] <= max_y:
                    n += 1
                    if resonance or dist(np, p1) == 2 * dist(np, p2):
                        results.add(np)

                else:
                    break
    return results


antenna_types, max_x, max_y = read_antennas("day08_input")
res = get_antinodes(antenna_types, max_x, max_y)
s = ""
an = set()
for at in antenna_types:
    for el in antenna_types[at]:
        an.add((at, el))
for y in range(max_y + 1):
    for x in range(max_x + 1):
        name = "."
        for a in an:
            if a[1][0] == x and a[1][1] == y:
                name = a[0]
        s += name
    s += "\n"
print(s)
s = ""
for y in range(max_y + 1):
    for x in range(max_x + 1):
        s += (((x, y) in res) and "#") or (".")
    s += "\n"
print(s)
print(len(res))


res = get_antinodes(antenna_types, max_x, max_y, resonance=True)
s = ""
for y in range(max_y + 1):
    for x in range(max_x + 1):
        s += (((x, y) in res) and "#") or (".")
    s += "\n"
print(s)

print(len(res))
