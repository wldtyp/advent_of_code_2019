import fileinput

from collections import *
from itertools import *
from functools import *
from more_itertools import *
import sys
import math
import copy


def get_input():
    life = {}
    for y, l in enumerate(fileinput.input()):
        for x, c in enumerate(l.strip()):
            life[(x, y)] = c
    return life


life = get_input()


def print_life(life):
    for y in range(5):
        for x in range(5):
            print(life[(x, y)], end="")
        print("")
    print("")


def calc_value(life):
    return sum(2 ** i for i, v in enumerate(life.values()) if v == "#")


seen = set()

for x in range(200):
    bugs_coords = frozenset(k for k, v in life.items() if v == "#")
    if bugs_coords in seen:
        print(calc_value(life))
        break
    else:
        seen.add(bugs_coords)

    next_step = {}
    for coords in life.keys():
        x, y = coords
        nearby = 0
        for to_check in [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]:
            if to_check in life and life[to_check] == "#":
                nearby += 1

        if life[coords] == "#":
            next_step[coords] = "#" if nearby == 1 else "."
        else:
            next_step[coords] = "#" if nearby == 1 or nearby == 2 else "."
    life = next_step
    # print_life(life)
