import functools

test_stones = [125, 17]
rules = [
    (lambda x: x == 0, lambda x: [1]),
    (
        lambda x: len(str(x)) % 2 == 0,
        lambda x: [int(str(x)[: len(str(x)) // 2]), int(str(x)[len(str(x)) // 2 :])],
    ),
    (lambda x: True, lambda x: [x * 2024]),
]


def next_stone(stone):
    for check, apply in rules:
        if check(stone[0]):
            return [(a, stone[1] - 1) for a in apply(stone[0])]


# @tail_recursion
@functools.cache
def blink(s):
    return (s[1] == 0 and 1) or sum([blink(x) for x in next_stone(s)])


stones = [5, 89749, 6061, 43, 867, 1965860, 0, 206250]

iterations = 25
stones_25 = list(zip(stones, [iterations] * len(stones)))
result = sum([blink(s) for s in stones_25])

print("result: ", result)

iterations = 75
stones_75 = list(zip(stones, [iterations] * len(stones)))
result = sum([blink(s) for s in stones_75])

print("result: ", result)
