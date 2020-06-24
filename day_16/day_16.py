import fileinput
from itertools import *


TEN_K = 10_000


def get_input():
    return [int(x) for x in next(fileinput.input())]


def to_string(int_array):
    return "".join((str(d) for d in int_array))


phase = get_input()
offset = int(to_string(phase[:7]))
phase_2 = phase.copy() * TEN_K
phase_2 = phase_2[offset:]


def gen_pattern_for(n):
    pattern = []
    pattern += [0] * n
    pattern += [1] * n
    pattern += [0] * n
    pattern += [-1] * n
    pattern = cycle(pattern)
    next(pattern)
    return pattern


input_length = len(phase)
for phase_number in range(1, 101):
    new_phase = [0] * input_length
    for i, value in enumerate(phase):
        pattern = gen_pattern_for(i + 1)
        new_phase[i] = abs(sum(a * b for a, b in zip(phase, pattern))) % 10
    phase = new_phase

print(f"Part 1: {to_string(phase[:8])}")


input_length = len(phase_2)
for phase_number in range(1, 101):
    new_phase = [0] * input_length
    total = sum(phase_2)
    for i, value in enumerate(phase_2):
        new_phase[i] = total % 10
        total = total - value
    phase_2 = new_phase

print(f"Part 2: {to_string(phase_2[:8])}")
