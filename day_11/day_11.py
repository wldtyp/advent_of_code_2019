import sys

sys.path.append("../")

from collections import *
from itertools import *
from functools import *
from more_itertools import *
import fileinput

from int_code_machine import IntCodeMachine as ICM


def get_input():
    contents = next(fileinput.input())
    return [int(x) for x in contents.split(",")]


grid = defaultdict(int)
current_position = (0, 0)
current_direction = "up"
grid[current_position] = 1

turns = {
    "up": {0: "left", 1: "right",},
    "right": {0: "up", 1: "down",},
    "down": {0: "right", 1: "left",},
    "left": {0: "down", 1: "up",},
}


def move(current_position, direction):
    x, y = current_position
    if direction == "up":
        y = y + 1
    elif direction == "right":
        x = x + 1
    elif direction == "down":
        y = y - 1
    elif direction == "left":
        x = x - 1
    return (x, y)


data = get_input()
paint_bot = ICM(data)
paint_bot.run()

while not paint_bot.state == ICM.HALT:
    paint_bot.input(grid[current_position])
    colour = paint_bot.output()
    left_or_right = int(paint_bot.output())
    grid[current_position] = colour
    current_direction = turns[current_direction][left_or_right]
    current_position = move(current_position, current_direction)

print(f"Squares visted: {len(grid)}")

max_x = max(p[0] for p in grid.keys())
min_x = min(p[0] for p in grid.keys())
max_y = max(p[1] for p in grid.keys())
min_y = min(p[1] for p in grid.keys())

for y in range(max_y, min_y - 1, -1):
    for x in range(min_x + 1, max_x + 1):
        colour = "X" if grid[(x, y)] else " "
        print(colour, end="")
    print("")
