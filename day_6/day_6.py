import fileinput
from collections import Counter


def get_input():
    return [x.strip().split(")") for x in fileinput.input()]


universe = dict(map(reversed, get_input()))


def path_to_COM(p):
    path = []
    while (p := universe[p]) in universe:
        path.append(p)
    return path + [p]


orbits = sum(len(path_to_COM(x)) for x in universe.keys())
print(f"orbits: {orbits}")

transfers = set(path_to_COM("YOU")) ^ set(path_to_COM("SAN"))
print(f"transfers: {len(transfers)}")
