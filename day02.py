from operator import sub

test_records = [
    [7, 6, 4, 2, 1],
    [1, 2, 7, 8, 9],
    [9, 7, 6, 2, 1],
    [1, 3, 2, 4, 5],
    [8, 6, 4, 4, 1],
    [1, 3, 6, 7, 9],
]


def check_safety_day(t):
    record = list(map(sub, t, [0] + t[:]))[1:]
    return (
        sum(
            [
                abs(record[i]) > 3 or record[i] * record[0] <= 0
                for i in range(len(record))
            ]
        )
        == 0
    )


def check_safety(data):
    n_safe = 0
    for t in data:
        if check_safety_day(t):
            n_safe += 1
    return n_safe


def check_safety_dampener(data):
    n_safe = 0
    for t in data:
        if sum([check_safety_day(t[:i] + t[i + 1 :]) for i in range(len(t))]) > 0:
            n_safe += 1
    return n_safe


with open("day02_input") as file:
    data = [list(map(int, line[:-1].split())) for line in file]

print("number of safe days: ", check_safety(data))
print("number of safe days with dampener: ", check_safety_dampener(data))
