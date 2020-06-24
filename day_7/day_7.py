import sys
sys.path.append("../")

from itertools import permutations
from itertools import cycle
from int_code_machine import IntCodeMachine


def get_input():
    with open(sys.argv[1]) as f:
        return [int(x) for x in f.read().split(",")]


phase_values = range(5)
all_phase_values = permutations(phase_values)


def run_amps(phase_values):
    output = 0
    for p in phase_values:
        data = get_input()
        amp = IntCodeMachine(data)
        amp.input(p)
        amp.input(output)
        output = amp.output()
    return output


all_runs = [run_amps(x) for x in all_phase_values]
print(f"Part 1: {max(all_runs)}")


phase_values = range(5, 10)
all_phase_values = permutations(phase_values)


def run_amps_looped(phase_values):
    amps = []
    for p in phase_values:
        data = get_input()
        amp = IntCodeMachine(data)
        amp.input(p)
        amps.append(amp)

    output = 0
    amps = cycle(amps)
    while (a := next(amps)).state != IntCodeMachine.HALT:
        a.input(output)
        output = a.output()
    return output


all_runs = [run_amps_looped(x) for x in all_phase_values]
print(f"Part 2: {max(all_runs)}")
