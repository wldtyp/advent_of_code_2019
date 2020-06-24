import sys
sys.path.append("../")
from int_code_machine import IntCodeMachine as ICM

from collections import *
from itertools import *
from functools import *
from more_itertools import *
import sys
import math


limit = 10000
grid = {}
SQUARE = 100
TRACTOR = ICM()

def beam(x,y):
    TRACTOR.reset()
    TRACTOR.run()
    TRACTOR.input(x)
    TRACTOR.input(y)
    out = TRACTOR.output()
    return out

def find_beam_on_row(y, start_x=0):
    beam_points = []
    x = start_x
    beam_started = False
    while not beam_started or in_beam:
        if in_beam := beam(x, y):
            beam_points.append((x,y))
            if not beam_started:
                beam_started = True
        x += 1
        if y * 2 < x:
            break 
    return beam_points

def wide_enough(first, last):
    width = (last - first)
    return width >= SQUARE

def square_fits_in_beam_at(x,y):
    top_left = beam(x, y)
    top_right = beam(x + SQUARE - 1, y)
    bottom_left = beam(x, y+SQUARE - 1)
    bottom_right = beam(x + SQUARE - 1, y+SQUARE-1)
    if all([top_left, top_right, bottom_left, bottom_right]):
        return True
    return False

def square_fits_on_row(y):
    b = find_beam_on_row(y, y)
    f = b[0][0]
    l = b[-1][0]
    if wide_enough(f,l):
        for x in range(f,l+1):
            if square_fits_in_beam_at(x, y):
                print(f"({x},{y}) -> {x*10000 + y}" )
                return x*10000 + y
    return False


count = 0
for y in range(50):
    print(f"{y}: \t", end='')
    b = find_beam_on_row(y)
    for x in range(50):
        if (x,y) in b:
            print('#', end='')
            count += 1
        else:
            print('.', end='')
    if b:
        print(f' {len(b)} \t{b[0][0]} to {b[-1][0]}')
    else:
        print(' 0 \tNone!')

print(f"Part 1: {count}")

print(f"Searching for Part 2:")
upper_limit = 2000
lower_limit = 0
best = 0
while upper_limit != lower_limit:
    guess = int((upper_limit + lower_limit) / 2)
    print(f"\t checking row {guess} for 100x100 square ...", end='')
    if answer := square_fits_on_row(guess):
        best = answer
        upper_limit = guess
    else:
        print('Nope!')
        lower_limit = guess + 1

print(f"Part 2: {best}")
