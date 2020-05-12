import fileinput


def get_input():
    contents = next(fileinput.input())
    return [int(x) for x in contents.split(",")]


PROGRAM = get_input()
ADD = 1
MULTIPLY = 2
INPUTOP = 3
OUTPUTOP = 4
JUMP_TRUE = 5
JUMP_FALSE = 6
LESS_THAN = 7
EQ = 8
HALT = 99


def add_op(data, a, b, r, modes):
    if modes[0] == 0:
        a = data[a]
    if modes[1] == 0:
        b = data[b]
    data[r] = a + b


def mult_op(data, a, b, r, modes):
    if modes[0] == 0:
        a = data[a]
    if modes[1] == 0:
        b = data[b]
    data[r] = a * b


def jump_true_op(data, a, b, modes):
    if modes[0] == 0:
        a = data[a]
    if modes[1] == 0:
        b = data[b]
    if a != 0:
        return b
    else:
        return None


def jump_false_op(data, a, b, modes):
    if modes[0] == 0:
        a = data[a]
    if modes[1] == 0:
        b = data[b]
    if a == 0:
        return b
    else:
        return None


def less_than_op(data, a, b, r, modes):
    if modes[0] == 0:
        a = data[a]
    if modes[1] == 0:
        b = data[b]
    if a < b:
        data[r] = 1
    else:
        data[r] = 0


def eq_op(data, a, b, r, modes):
    if modes[0] == 0:
        a = data[a]
    if modes[1] == 0:
        b = data[b]
    if a == b:
        data[r] = 1
    else:
        data[r] = 0


def input_op(data, a, input_value):
    print(f"input \t{input_value}")
    data[a] = input_value


def output_op(data, a, modes):
    if modes[0] == 0:
        output = data[a]
    else:
        output = a
    print(f"output \t{output}")


def op_code_and_mode(op_code):
    op_code = str(op_code)
    new_op_code = int(op_code[-2:])
    modes = [int(x) for x in op_code[:-2]]
    return new_op_code, list(reversed(modes)) + [0, 0, 0, 0]


def run(input_value):
    data = PROGRAM.copy() + [0, 0, 0, 0, 0, 0]
    head = 0
    op_code, a, b, r = data[head : head + 4]
    op_code, modes = op_code_and_mode(op_code)
    while op_code != HALT:
        if op_code == ADD:
            add_op(data, a, b, r, modes)
            head += 4
        if op_code == MULTIPLY:
            mult_op(data, a, b, r, modes)
            head += 4
        if op_code == INPUTOP:
            input_op(data, a, input_value)
            head += 2
        if op_code == OUTPUTOP:
            output_op(data, a, modes)
            head += 2
        if op_code == JUMP_TRUE:
            new_head = jump_true_op(data, a, b, modes)
            if new_head:
                head = new_head
            else:
                head += 3
        if op_code == JUMP_FALSE:
            new_head = jump_false_op(data, a, b, modes)
            if new_head:
                head = new_head
            else:
                head += 3
        if op_code == LESS_THAN:
            less_than_op(data, a, b, r, modes)
            head += 4
        if op_code == EQ:
            eq_op(data, a, b, r, modes)
            head += 4
        op_code, a, b, r = data[head : head + 4]
        op_code, modes = op_code_and_mode(op_code)


print("Part 1")
run(1)
print("Part 2")
run(5)
