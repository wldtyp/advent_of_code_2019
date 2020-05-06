import fileinput


def get_input():
    contents = next(fileinput.input())
    return [int(x) for x in contents.split(",")]


PROGRAM = get_input()
ADD = 1
MULTIPLY = 2
HALT = 99


def add_op(data, a, b, r):
    data[r] = data[a] + data[b]


def mult_op(data, a, b, r):
    data[r] = data[a] * data[b]


def run(noun, verb):
    data = PROGRAM.copy()
    data[1] = noun
    data[2] = verb
    head = 0
    op_code, a, b, r = data[head : head + 4]
    while op_code != HALT:
        if op_code == ADD:
            add_op(data, a, b, r)
        if op_code == MULTIPLY:
            mult_op(data, a, b, r)
        head += 4
        op_code, a, b, r = data[head : head + 4]
    return data[0]


print(f"Part 1: {run(12,2)}")

UPPER_LIMIT = 100
for x in range(0, UPPER_LIMIT):
    for y in range(0, UPPER_LIMIT):
        if run(x, y) == 19690720:
            print(f"Part 2: {100 * x + y}")
