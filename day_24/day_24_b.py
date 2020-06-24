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
            life[(x, y, 0)] = c
    return life


life = get_input()


def print_life(life):
    min_z = min(z for x, y, z in life.keys())
    max_z = max(z for x, y, z in life.keys())
    for z in range(min_z, max_z + 1):
        print(f"Depth {z}:")
        for y in range(5):
            for x in range(5):
                print(life[(x, y, z)], end="")
            print("")
        print("")


for x in range(200):
    next_step = {}
    min_z = min(z for x, y, z in life.keys())
    max_z = max(z for x, y, z in life.keys())
    for z in range(min_z - 1, max_z + 2):
        for y in range(5):
            for x in range(5):
                nearby = 0
                if x == 2 and y == 2:
                    next_step[(x, y, z)] = "?"
                    continue

                to_check = [(x, y - 1, z), (x - 1, y, z), (x + 1, y, z), (x, y + 1, z)]

                if x == 0:
                    to_check.append((1, 2, z + 1))
                if x == 4:
                    to_check.append((3, 2, z + 1))
                if y == 0:
                    to_check.append((2, 1, z + 1))
                if y == 4:
                    to_check.append((2, 3, z + 1))

                if (x, y) == (2, 1):
                    to_check.extend([(new_x, 0, z - 1) for new_x in range(5)])
                if (x, y) == (2, 3):
                    to_check.extend([(new_x, 4, z - 1) for new_x in range(5)])
                if (x, y) == (1, 2):
                    to_check.extend([(0, new_y, z - 1) for new_y in range(5)])
                if (x, y) == (3, 2):
                    to_check.extend([(4, new_y, z - 1) for new_y in range(5)])

                for p in to_check:
                    if p in life and life[p] == "#":
                        nearby += 1

                if (x, y, z) in life and life[(x, y, z)] == "#":
                    next_step[(x, y, z)] = "#" if nearby == 1 else "."
                else:
                    next_step[(x, y, z)] = "#" if nearby in (1, 2) else "."
    life = next_step

print(sum(1 for v in life.values() if v == "#"))
