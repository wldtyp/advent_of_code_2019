import fileinput


def get_input():
    for l in fileinput.input():
        yield l.strip().split(",")


def wire_to_points(instructions):
    steps = 0
    lowest = {(0, 0): 0}
    points = [(0, 0)]
    for i in instructions:
        direction, distance = i[0], int(i[1:])
        for _ in range(distance):
            steps += 1
            x, y = points[-1]
            if direction == "U":
                next_point = (x + 1, y)
            if direction == "D":
                next_point = (x - 1, y)
            if direction == "R":
                next_point = (x, y + 1)
            if direction == "L":
                next_point = (x, y - 1)
            if next_point not in lowest:
                lowest[next_point] = steps
            points.append(next_point)
    return set(points), lowest


wires = get_input()
wire_one, lowest_one = wire_to_points(next(wires))
wire_two, lowest_two = wire_to_points(next(wires))

common_points = wire_one.intersection(wire_two)
manhat = [abs(p[0]) + abs(p[1]) for p in common_points]
signal_time = [lowest_one[p] + lowest_two[p] for p in common_points]

print(f"Part 1: {sorted(manhat)[1]}")
print(f"Part 2: {sorted(signal_time)[1]}")
