import fileinput
from collections import *
from itertools import *
from functools import *
from more_itertools import *
import math


def get_input():
    return [x.strip() for x in fileinput.input()]


empty = set()
asteriods = set()

data = get_input()
for y, row in enumerate(data):
    for x, point in enumerate(row):
        if point == ".":
            empty.add((x, y))
        else:
            asteriods.add((x, y))


def dist(p1, p2):
    d = pow((p1[1] - p2[1]), 2) + pow((p1[0] - p2[0]), 2)
    return math.sqrt(d)


def angle(p1, p2):
    a = math.degrees((math.atan2(p1[1] - p2[1], p1[0] - p2[0])))
    a += 90
    if a < 0:
        return 90 + a + 270
    return a


def nearest_only(origin, asteriods):
    left = asteriods.copy()
    in_order = [(angle(p, origin), dist(p, origin), p) for p in asteriods]
    in_order_sorted = sorted(in_order)
    in_order_grouped = groupby(in_order_sorted, key=lambda x: x[0])
    for _, on_line in in_order_grouped:
        to_drop = [p[2] for p in list(on_line)[1:]]
        for drop in to_drop:
            left.discard(drop)
    return left


def visable_count(origin, asteriods):
    return len(nearest_only(origin, asteriods))


all_points = [(visable_count(p, asteriods), p) for p in asteriods]
best = max(all_points)

origin = best[1]
nearest = nearest_only(origin, asteriods)
in_order = [(angle(p, origin), p) for p in nearest]
in_order_sorted = sorted(in_order)
count = 0
for theta, point in in_order_sorted:
    count += 1
    print(f"{count} {theta} {point}")

print(f"Part 1: {count}")
two_hundred = in_order_sorted[199]
x, y = two_hundred[1]
print(f"Part 2: {x*100 + y}")
