import sys

sys.path.append("../")

import fileinput
from collections import *
from itertools import *
from functools import *
from more_itertools import *

import math

from int_code_machine import IntCodeMachine as ICM


def get_input():
    contents = next(fileinput.input())
    return [int(x) for x in contents.split(",")]


# north (1), south (2), west (3), and east (4)

# 0: The repair droid hit a wall. Its position has not changed.
# 1: The repair droid has moved one step in the requested direction.
# 2: The repair droid has moved one step in the requested direction; its new position is the location of the oxygen system.

back = {1: 2, 2: 1, 3: 4, 4: 3}

data = get_input()

repair_driod = ICM(data)
repair_driod.run()


current = (0, 0)
grid = defaultdict(list)
grid[current] = []
to_explore = []
to_explore.append((0, 0))
explored = set(current)


def new_cell(location, direction):
    x, y = location
    if direction == 1:
        return (x, y + 1)
    if direction == 2:
        return (x, y - 1)
    if direction == 3:
        return (x - 1, y)
    if direction == 4:
        return (x + 1, y)


def explore(location, path):
    direction = path[-1]
    repair_driod.input(direction)
    result = repair_driod.output()
    if result > 0:
        repair_driod.input(back[direction])
        repair_driod.output()
    return new_cell(location, direction), result


def go(path):
    for n in path:
        repair_driod.input(n)
        repair_driod.output()


def backtrack(path):
    for n in path[::-1]:
        repair_driod.input(back[n])
        repair_driod.output()


path = []
oxygen_cell = None

while to_explore:
    try:
        cell = to_explore.pop(0)
        path = grid[cell]
        go(path)
        for n in range(1, 5):
            new_path = path.copy()
            new_path.append(n)
            next_cell, kind = explore(cell, new_path)
            if next_cell != current:
                if kind == 0:
                    explored.add(next_cell)
                elif (kind == 1 or kind == 2) and next_cell not in explored:
                    if next_cell:
                        to_explore.append(next_cell)
                        grid[next_cell] = new_path
                if kind == 2:
                    oxygen_cell = next_cell
                    print(f"Part 1: {next_cell}, {len(new_path)}")
        explored.add(cell)
        backtrack(path)
    except:
        pass

starting_point = oxygen_cell
grid = set(grid.keys())

explored = {starting_point: 0}
max_length = 0
to_explore = [starting_point]
while to_explore:
    current = to_explore.pop(0)
    depth = explored[current]
    for n in range(1, 5):
        p = new_cell(current, n)
        if p in grid:
            explored[p] = depth + 1
            grid.remove(p)
            to_explore.append(p)
print(f"Part 2: {max(explored.values())}")
