import fileinput

from collections import *
from itertools import *
from heapq import *


def get_input():
    return [x.strip() for x in fileinput.input()]


maze = {}
for y, row in enumerate(get_input()):
    for x, c in enumerate(row):
        maze[(x, y)] = c
        if c == "@":
            origin = (x, y)

key_positions = {v: k for k, v in maze.items() if v.isalpha() and v.islower()}
key_positions["@"] = origin
all_keys = frozenset(key_positions.keys())
door_positions = {v: k for k, v in maze.items() if v.isalpha() and v.isupper()}


def find_path(a, b, maze, steps=0):
    q = []
    heapify(q)
    heappush(q, (steps, [a]))
    explored = set()
    while q:
        steps, path = heappop(q)
        a = path[-1]
        explored.add(a)
        x, y = a
        if a == b:
            return steps, path

        def process(point):
            if point not in explored and maze[point] != "#":
                new_path = path.copy()
                new_path.append(point)
                heappush(q, (steps + 1, new_path))

        process((x + 1, y))
        process((x - 1, y))
        process((x, y + 1))
        process((x, y - 1))


def get_required_keys_on_path(path):
    doors = [k for k, v in door_positions.items() if v in path]
    to_keys = [d.lower() for d in doors]
    return filter(lambda k: k in all_keys, to_keys)


graph = defaultdict(list)
for key_a, key_b in combinations(sorted(all_keys), 2):
    a, b = key_positions[key_a], key_positions[key_b]
    steps, path = find_path(a, b, maze)
    if not any(maze[x].islower() or maze[x] == "@" for x in path[1:-1]):
        doors = frozenset(get_required_keys_on_path(path))
        graph[key_a].append((steps, key_b, doors))
        graph[key_b].append((steps, key_a, doors))


paths = []
heapify(paths)
heappush(paths, (0, "@", frozenset("@")))
fastest = defaultdict(int)

while paths:
    steps, node, collected = heappop(paths)
    if collected == all_keys:
        print(steps)
        break
    for dist, adj_node, req in graph[node]:
        if req <= collected:
            new_collected = collected | frozenset([adj_node])
            total_dist = steps + dist
            best_so_far = fastest[(adj_node, new_collected)]
            if not best_so_far or total_dist < best_so_far:
                fastest[(adj_node, new_collected)] = total_dist
                heappush(paths, (total_dist, adj_node, new_collected))

