import re
import functools

test_string = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"

with open("day03_input") as file:
    input = file.read()

operations = re.findall("mul\([0-9]+,[0-9]+\)", input)
print(
    sum(
        [
            functools.reduce(lambda x, y: int(x) * int(y), re.findall("[0-9]+", op))
            for op in operations
        ]
    )
)

test_string = (
    "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
)
operations2 = re.findall("don't\(\)|do\(\)|mul\([0-9]+,[0-9]+\)", input)
print(operations2)
skip = False
sum = 0
for o in operations2:
    match o:
        case "don't()":
            skip = True
        case "do()":
            skip = False
        case op:
            if not skip:
                sum += functools.reduce(
                    lambda x, y: int(x) * int(y), re.findall("[0-9]+", op)
                )

print(sum)
