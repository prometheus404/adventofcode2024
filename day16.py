from io import open_code


directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
maze = {"#": set(), "S": set(), "E": set(), ".": set()}


def move(p, d):
    return (p[0] + d[0], p[1] + d[1])


def turn(d, cclock=False):
    if cclock:
        return directions[(directions.index(d) - 1) % len(directions)]
    else:
        return directions[(directions.index(d) + 1) % len(directions)]


def legal(p):
    return p not in maze["#"]


class Graph(object):
    nodes = set()
    edges = set()  # for a better implementation this should be a dict of sets

    def __init__(self, maze) -> None:
        # node structure: (position, direction)
        self.nodes.update([(p, d) for p in maze["."] for d in directions])
        self.nodes.update([(p, d) for p in maze["S"] for d in directions])
        self.nodes.update([(p, d) for p in maze["E"] for d in directions])
        # edge structure: (node1,node2,cost)
        self.edges.update(
            [
                (n, (move(n[0], n[1]), n[1]), 1)
                for n in self.nodes
                if legal(move(n[0], n[1]))
            ]
        )  # forward movement
        self.edges.update(
            [(n, (n[0], turn(n[1])), 1000) for n in self.nodes]
        )  # clockwise turn
        self.edges.update(
            [(n, (n[0], turn(n[1], cclock=True)), 1000) for n in self.nodes]
        )  # cclockwise turn
        print(self.nodes)
        print(self.edges)

    def get_neighbor(self, node):
        return [(x[1], x[2]) for x in self.edges if x[0] == node]


def euclidean_distance(p, q):
    return ((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2) ** (1 / 2)


def rotation_distance(r1, r2):
    return (
        (r1 == r2 and 0)
        or (turn(r1) == r2 and 1000)
        or (r1 == turn(r2) and 1000)
        or 2000
    )


def heuristic(n1, n2):
    return euclidean_distance(n1[0], n2)


def a_star(graph, start, end, h):
    def reconstruct_path(current):
        total_path = [current]
        while current in came_from.keys():
            current = came_from[current]
            total_path = [current] + total_path
        return total_path

    open_set = [start]
    came_from = {}
    g_score = {}
    f_score = {}
    for n in graph.nodes:
        g_score[n] = 2**1000  # initialize to "infinity"
        f_score[n] = 2**1000

    g_score[start] = 0
    print(start)
    f_score[start] = h(start, end)

    while len(open_set) > 0:
        # (print(o, g_score[o], f_score[o]) for o in open_set)
        open_set.sort(key=lambda x: f_score[x])
        current = open_set[0]
        # print("curr", current)
        if current[0] == end:
            return reconstruct_path(current), g_score[current]
        open_set = open_set[1:]
        for neighbor, distance in graph.get_neighbor(current):
            tentative_g_score = g_score[current] + distance
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + h(neighbor, end)
                if neighbor not in open_set:
                    open_set.append(neighbor)
                    # print(open_set)
    return (0, 0)


def score(p):
    sum([1 if p[x][0] != p[x - 1][0] else 1000 for x in range(2, len(p))])


if __name__ == "__main__":
    test = False
    filename = "day16_input"
    if test:
        filename += "_test"
    with open(filename) as file:
        y = 0
        for line in file:
            x = 0
            for char in line:
                (char != "\n" and maze[char].update([(x, y)]))
                x += 1
            y += 1
    g = Graph(maze)
    path, score = a_star(g, (maze["S"].pop(), (1, 0)), maze["E"].pop(), heuristic)
    print(path)
    print(score)
