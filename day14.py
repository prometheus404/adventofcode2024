import re

test_txt = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""
# test_txt = "p=2,4 v=2,-3"


def read(text):
    acc = set()
    for line in text:
        print(line)
        m = re.match(r"p=(.*),(.*) v=(.*),(.*)", line)
        acc.update(
            [((int(m.group(1)), int(m.group(2))), (int(m.group(3)), int(m.group(4))))]
        )
    return acc


def move(robots, max_x, max_y):
    return {
        (
            ((r[0][0] + r[1][0]) % max_x, (r[0][1] + r[1][1]) % max_y),
            r[1],
        )
        for r in robots
    }


def draw(robots, max_x, max_y):
    map = [
        [
            len([1 for r in robots if (r[0][0] == x and r[0][1] == y)])
            for x in range(max_x)
        ]
        for y in range(max_y)
    ]
    s = ""
    for i in map:
        for j in i:
            s += str(j) if j > 0 else "."
        s += "\n"
    print(s)


def safety_factor(robots, max_x, max_y):
    q0 = q1 = q2 = q3 = 0
    for r in robots:
        q0 += r[0][0] < max_x // 2 and r[0][1] < max_y // 2 and 1
        q1 += r[0][0] > max_x // 2 and r[0][1] < max_y // 2 and 1
        q2 += r[0][0] < max_x // 2 and r[0][1] > max_y // 2 and 1
        q3 += r[0][0] > max_x // 2 and r[0][1] > max_y // 2 and 1
    return q0 * q1 * q2 * q3


if __name__ == "__main__":
    test = False
    if test:
        robots = read(test_txt.split("\n"))
        max_x = 11
        max_y = 7
    else:
        with open("day14_input") as file:
            robots = read(file)
            max_x = 101
            max_y = 103
    print("initial state:")
    draw(robots, max_x, max_y)
    for i in range(100):
        robots = move(robots, max_x, max_y)
        print("after", i + 1, "seconds")
        # draw(robots, max_x, max_y)
    minimum = (100, safety_factor(robots, max_x, max_y))
    print(minimum)
    for i in range(101, 10000):
        robots = move(robots, max_x, max_y)
        s = safety_factor(robots, max_x, max_y)
        if s < minimum[1]:
            minimum = (i, safety_factor(robots, max_x, max_y))
            draw(robots, max_x, max_y)
            print("iteration:", i)
