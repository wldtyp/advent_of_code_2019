import fileinput

from collections import *
from itertools import *
from functools import *
from more_itertools import *
import sys
import math
from heapq import *


def get_input():
    return [x for x in fileinput.input()]


maze = {}
portals = {}
for y, row in enumerate(get_input()):
    for x, c in enumerate(row[:-1]):
        if c == ".":
            maze[(x, y)] = c
        if c.isupper():
            portals[(x, y)] = c

max_x, max_y = x, y
portal_pairs = defaultdict(list)

for p in portals.keys():
    x, y = p
    v = portals[p]
    if v.isupper():
        right = (x + 1, y)
        left = (x - 1, y)
        up = (x, y - 1)
        down = (x, y + 1)
        if right in portals:
            key = portals[p] + portals[right]
            if left in maze:
                portal_pairs[key].append(left)
                maze[left] = key
            else:
                portal_pairs[key].append((x + 2, y))
                maze[(x + 2, y)] = key
        if down in portals:
            key = portals[p] + portals[down]
            if up in maze:
                portal_pairs[key].append(up)
                maze[up] = key
            else:
                maze[(x, y + 2)] = key
                portal_pairs[key].append((x, y + 2))

origin = portal_pairs["AA"][0]
del portal_pairs["AA"]
target = portal_pairs["ZZ"][0]
del portal_pairs["ZZ"]


def find_path(a, b, maze, portal_pairs):
    start = (a[0], a[1])
    q = deque([(0, start)])
    b = (b[0], b[1])
    explored = set()
    while q:
        steps, a = q.popleft()
        explored.add(a)
        x, y = a
        if a == b:
            return steps

        def exit_portal(point):
            x, y = point
            key = maze[(x, y)]
            portal_a, portal_b = portal_pairs[key]
            if (x, y) == portal_a:
                return (portal_b[0], portal_b[1])
            else:
                return (portal_a[0], portal_a[1])

        def process(point):
            x, y = point
            if point not in explored and (x, y) in maze:
                symbol = maze[(x, y)]
                if symbol == ".":
                    new_steps = steps + 1
                elif symbol == "AA":
                    return
                elif symbol == "ZZ":
                    new_steps = steps + 1
                elif symbol.isalpha():
                    p = exit_portal(point)
                    if p is None:
                        return
                    point = p
                    new_steps = steps + 2
                q.append((new_steps, point))

        process((x + 1, y))
        process((x - 1, y))
        process((x, y + 1))
        process((x, y - 1))


def find_recursive_path(a, b, maze, portal_pairs):
    start = (a[0], a[1], 0)
    q = deque([(0, start)])
    b = (b[0], b[1], 0)
    explored = set()
    while q:
        steps, a = q.popleft()
        explored.add(a)
        x, y, z = a
        if a == b:
            return steps

        def exit_portal(point):
            x, y, z = point
            key = maze[(x, y)]
            portal_a, portal_b = portal_pairs[key]
            if 4 < x < max_x - 4 and 4 < y < max_y - 4:
                new_depth = z + 1
            else:
                new_depth = z - 1
            if new_depth < 0:
                return None
            if (x, y) == portal_a:
                return (portal_b[0], portal_b[1], new_depth)
            else:
                return (portal_a[0], portal_a[1], new_depth)

        def process(point):
            x, y, depth = point
            if point not in explored and (x, y) in maze:
                symbol = maze[(x, y)]
                if symbol == ".":
                    new_steps = steps + 1
                elif symbol == "AA":
                    return
                elif symbol == "ZZ":
                    if depth > 0:
                        return
                    new_steps = steps + 1
                elif symbol.isalpha():
                    p = exit_portal(point)
                    if p is None:
                        return
                    point = p
                    new_steps = steps + 2
                q.append((new_steps, point))

        process((x + 1, y, z))
        process((x - 1, y, z))
        process((x, y + 1, z))
        process((x, y - 1, z))


print(f"Part 1: {find_path(origin, target, maze, portal_pairs)}")
print(f"Part 2: {find_recursive_path(origin, target, maze, portal_pairs)}")
