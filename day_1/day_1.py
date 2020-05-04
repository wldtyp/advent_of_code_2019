import fileinput


def get_input():
    for l in fileinput.input():
        yield int(l.strip())


def calculate_fuel(mass):
    return mass // 3 - 2


def calculate_total_fuel(mass):
    required_fuel = calculate_fuel(mass)
    if required_fuel < 0:
        return 0
    else:
        return required_fuel + calculate_total_fuel(required_fuel)


total = sum(calculate_fuel(mass) for mass in get_input())
second_total = sum(calculate_total_fuel(mass) for mass in get_input())

print(f"Part 1: {total}")
print(f"Part 2: {second_total}")
