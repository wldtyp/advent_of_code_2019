import sys

sys.path.append("../")


from int_code_machine import IntCodeMachine as ICM

ASCII = ICM()
ASCII.run()

x = 0
y = 0
grid = {}
while c := ASCII.output_ascii():
    print(c, end="")
    if ord(c) == 10:
        y += 1
        x = 0
    else:
        grid[(x, y)] = c
        x += 1


def intersection(point, grid):
    x, y = point
    if grid[(x, y)] != "#":
        return False
    try:
        if grid[(x - 1, y)] != "#":
            return False
        if grid[(x + 1, y)] != "#":
            return False
        if grid[(x, y + 1)] != "#":
            return False
        if grid[(x, y - 1)] != "#":
            return False
        return True
    except:
        return False


points = []
for y in range(39):
    for x in range(63):
        if intersection((x, y), grid):
            points.append((x, y))

print(f"Part 1: {sum((x * y for x, y in points))}")

print("Part 2:")

main = "A,A,B,C,B,C,B,C,B,A"
A = "R,6,L,12,R,6"
B = "L,12,R,6,L,8,L,12"
C = "R,12,L,10,L,10"
Video = "n"

ASCII.reset()
ASCII.data[0] = 2
ASCII.run()

try:
    while c := ASCII.output_ascii():
        print(c, end="")
except:
    pass

ASCII.input_ascii(main)
ASCII.input_ascii(A)
ASCII.input_ascii(B)
ASCII.input_ascii(C)
ASCII.input_ascii(Video)

try:
    while c := ASCII.output_ascii():
        print(c, end="")
except:
    pass

# Exit with newline
print()
