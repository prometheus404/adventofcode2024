test_list1 = [3, 4, 2, 1, 3, 3]
test_list2 = [4, 3, 5, 3, 9, 3]


def distance(l1, l2):
    return sum([abs(sorted(l1)[i] - sorted(l2)[i]) for i in range(len(l1))])


def similarity(l1, l2):
    return sum([x * sum([y == x for y in l2]) for x in l1])


with open("day1_input") as input:
    l1, l2 = zip(*[i[:-1].split("   ") for i in input])
    l1 = [int(i) for i in l1]
    l2 = [int(i) for i in l2]

print("distance between two lists: ", distance(l1, l2))

print("similarity between two lists: ", similarity(l1, l2))
