from collections import Counter
import fileinput


def get_input():
    for l in fileinput.input():
        start, stop = map(int, l.strip().split("-"))
        return (start, stop)


def has_double(x):
    c = Counter(x)
    return any(y > 1 for y in c.values())


def iso_double(x):
    c = Counter(x)
    return any(y == 2 for y in c.values())


def monotonic(x):
    return list(x) == sorted(x)


first, last = get_input()
count = 0
part_2_count = 0

for n in filter(monotonic, map(str, range(first, last + 1))):
    if has_double(n):
        count += 1
    if iso_double(n):
        part_2_count += 1

print(f"Part 1: {count}")
print(f"Part 2: {part_2_count}")
