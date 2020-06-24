import fileinput
from collections import *
from math import *


TRILLION = 1000000000000
reaction_for = {}


def parse_chemical(string):
    quantity, chemical = string.strip().split(" ")
    return (chemical, int(quantity))


for line in fileinput.input():
    reaction = {}
    reactants, product = line.strip().split("=>")
    reaction["reactants"] = [parse_chemical(c) for c in reactants.split(",")]
    reaction["product"] = parse_chemical(product)
    reaction_for[reaction["product"][0]] = reaction


def make_fuel(fuel_target, starting_ore):
    ore_cost = 0
    stockpile = defaultdict(int)
    required_products = defaultdict(int)
    required_products["FUEL"] = fuel_target
    while product := next(iter(required_products), None):
        required_quantity = required_products.pop(product)
        if product == "ORE":
            ore_cost += required_quantity
            if ore_cost > starting_ore:
                return False
            continue
        rxn = reaction_for[product]
        if product in stockpile:
            if stockpile[product] > required_quantity:
                stockpile[product] -= required_quantity
                required_quantity = 0
            else:
                required_quantity = required_quantity - stockpile[product]
                del stockpile[product]
        if required_quantity:
            rxn_yield = rxn["product"][1]
            required_runs = ceil(required_quantity / rxn_yield)
            total_ = required_runs * rxn_yield
            left_over_product = total_ - required_quantity
            if left_over_product:
                stockpile[product] += left_over_product
            for reactant, reactant_quantity in rxn["reactants"]:
                required_products[reactant] += reactant_quantity * required_runs
    return ore_cost


print(f"Cost to make 1 Fuel: {make_fuel(1,TRILLION)}")

lower_bound = 0
upper_bound = TRILLION
while True:
    fuel_target = lower_bound + (upper_bound - lower_bound) // 2
    if lower_bound == fuel_target:
        print(f"Max Possible Fuel: {fuel_target}")
        break
    result = make_fuel(fuel_target, TRILLION)
    if result:
        lower_bound = fuel_target
    else:
        upper_bound = fuel_target
