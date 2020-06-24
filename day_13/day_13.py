import sys

sys.path.append("../")

import fileinput
from collections import *

from int_code_machine import IntCodeMachine as ICM


arcade = ICM()


def run():
    arcade.run()
    screen = defaultdict(int)
    score = 0
    paddle_postion = (1, 0)
    ball_postion = (1, 0)
    game_started = False
    while not arcade.state == ICM.HALT:
        if arcade.state == ICM.INPUT:
            game_started = True
            if ball_postion[0] > paddle_postion[0]:
                arcade.input(1)
            elif ball_postion[0] < paddle_postion[0]:
                arcade.input(-1)
            else:
                arcade.input(0)
        x = arcade.output()
        y = arcade.output()
        if x == -1 and y == 0:
            score = arcade.output()
        else:
            t = arcade.output()
            if t == 3:
                paddle_postion = (x, y)
            if t == 4:
                ball_postion = (x, y)
            screen[(x, y)] = t
        c = Counter(screen.values())
    return c[2] if c[2] else score


print(f"Part 1: {run()}")
arcade.reset()
arcade.data[0] = 2
print(f"Part 2: {run()}")
