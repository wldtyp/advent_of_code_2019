import fileinput

from collections import *
from itertools import *
from functools import *
from more_itertools import *
import sys
import math
from heapq import *


def get_input():
    for line in fileinput.input():
        if "deal into new stack" in line:
            yield ("NEW", None)
        else:
            line = line.strip().split()
            action = "DEAL" if line[0] == "deal" else "CUT"
            yield (action, int(line[-1]))


shuffle_pattern = list(get_input())


def new_stack(deck, n=None):
    return list(reversed(deck))


def cut(deck, n):
    return deck[n:] + deck[:n]


def increment(deck, n):
    new_deck = [None] * len(deck)
    for i, card in enumerate(deck):
        new_index = i * n % len(deck)
        new_deck[new_index] = card
    return new_deck


functions = {"NEW": new_stack, "DEAL": increment, "CUT": cut}

deck = list(range(10007))
for fn, n in shuffle_pattern:
    new_deck = functions[fn](deck, n)
    deck = new_deck

print(f"Part 1: {deck.index(2019)}")


def new_stack_parameters(m, b, n=None):
    m *= -1
    b += m
    return m, b


def cut_parameters(m, b, n=None):
    b += n * m
    return m, b


def increment_parameters(m, b, n=None):
    m *= pow(n, -1, SPACE_CARDS)
    return m, b


compose_functions = {
    "NEW": new_stack_parameters,
    "DEAL": increment_parameters,
    "CUT": cut_parameters,
}

SPACE_CARDS = 119315717514047
SHUFFLES = 101741582076661
multiplication = 1
addition = 0


for fn, n in shuffle_pattern:
    multiplication, addition = compose_functions[fn](multiplication, addition, n)

total_multiplication = pow(multiplication, SHUFFLES, SPACE_CARDS)
total_addition = (
    addition * (1 - total_multiplication) * pow(1 - multiplication, -1, SPACE_CARDS)
)
print(f"Part 2: {(2020 * total_multiplication + total_addition) % SPACE_CARDS}")
