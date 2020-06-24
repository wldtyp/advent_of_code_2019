import fileinput


def get_input():
    return [x for x in next(fileinput.input())]


width, height = 25, 6


def take(iterable, n):
    return zip(*[iter(iterable)] * n)


layers = list(take(get_input(), height * width))
fewest_zeros = min(layers, key=lambda l: l.count("0"))
print(fewest_zeros.count("1") * fewest_zeros.count("2"))

img = [next(filter(lambda n: n != "2", stack)) for stack in zip(*layers)]
for row in take(img, width):
    print("".join(row).replace("0", " ").replace("1", "#"))
