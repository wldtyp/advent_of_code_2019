from copy import deepcopy
from dataclasses import dataclass
from itertools import *
from functools import *
import math

import fileinput


@dataclass
class Moon:
    x: int
    y: int
    z: int

    x_velocity: int = 0
    y_velocity: int = 0
    z_velocity: int = 0

    dimensions = ("x", "y", "z")

    @property
    def kenetic(self):
        return sum(map(abs, [self.x, self.y, self.z]))

    @property
    def potential(self):
        return sum(map(abs, [self.x_velocity, self.y_velocity, self.z_velocity]))

    @property
    def total(self):
        return self.kenetic * self.potential

    @property
    def x_component(self):
        return (self.x, self.x_velocity)

    @property
    def y_component(self):
        return (self.y, self.y_velocity)

    @property
    def z_component(self):
        return (self.z, self.z_velocity)

    def adjust_velocities(self, other_moon):
        for d in self.dimensions:
            self.adjust_velocity(other_moon, d)

    def adjust_velocity(self, other_moon, dimension):
        me, current_velocity = getattr(self, f"{dimension}_component")
        other = getattr(other_moon, dimension)
        if me > other:
            delta = -1
        elif me < other:
            delta = 1
        else:
            delta = 0
        setattr(self, f"{dimension}_velocity", current_velocity + delta)

    def move(self):
        for d in self.dimensions:
            current_position, current_velocity = getattr(self, f"{d}_component")
            setattr(self, d, current_position + current_velocity)


def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // math.gcd(a, b)


def lcmm(*args):
    """Return lcm of args."""
    return reduce(lcm, args)


moons = []

for line in fileinput.input():
    x, y, z = map(int, line.strip().split(","))
    moons.append(Moon(x, y, z))

starting_point = deepcopy(moons)
x, y, z = (None, None, None)
for n in range(1000000):
    if n == 1000:
        print(f"Part 1: {sum(m.total for m in moons)}")
    if all((x, y, z)):
        break
    pairs = combinations(moons, r=2)
    for a, b in pairs:
        a.adjust_velocities(b)
        b.adjust_velocities(a)
    for m in moons:
        m.move()
    if [m.x_component for m in moons] == [
        m.x_component for m in starting_point
    ] and not x:
        x = n + 1
    if [m.y_component for m in moons] == [
        m.y_component for m in starting_point
    ] and not y:
        y = n + 1
    if [m.z_component for m in moons] == [
        m.z_component for m in starting_point
    ] and not z:
        z = n + 1

print(moons)
print(x, y, z)
print(f"Part 2: {lcmm(x, y, z)}")
