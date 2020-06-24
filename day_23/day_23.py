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


NICs = {}
qs = defaultdict(list)
NAT = None
NAT_counter = Counter()
data = get_input()

for a in range(50):
    nic_at_address = ICM(data)
    nic_at_address.input(a)
    NICs[a] = nic_at_address

first = None
waiting = True
while waiting:
    for address in range(50):
        nic = NICs[address]
        if qs[address]:
            packet_x, packet_y = qs[address].pop(0)
            nic.input(packet_x)
            nic.input(packet_y)
            print(f"{address} recived: {packet_x} {packet_y}!")
        else:
            nic.input(-1)
        if len(nic.outputs) >= 3:
            a, x, y = nic.output(), nic.output(), nic.output()
            print(f"Sending {a}:{x},{y}")
            if a == 255:
                if first is None:
                    first = y
                NAT = (x, y)
            else:
                qs[a].append((x, y))
    if max(len(nic.outputs) for nic in NICs.values()) == 0:
        if max(len(q) for q in qs.values()) == 0:
            print(f"NAT sending {NAT}")
            qs[0].append(NAT)
            NAT_counter.update([NAT[1]])
            c = NAT_counter.most_common(1)
            if c[0][1] == 2:
                break

print(f"Part 1: {first}")
print(f"Part 2: {NAT_counter.most_common()[0][0]}")
