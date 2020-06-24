import sys

sys.path.append("../")

import fileinput

from int_code_machine import IntCodeMachine as ICM


def get_input():
    contents = next(fileinput.input())
    return [int(x) for x in contents.split(",")]


icm = ICM(get_input())
icm.input(1)
print(f"Part 1: {icm.output()}")

icm.reset()
icm.input(2)
print(f"Part 2: {icm.output()}")
