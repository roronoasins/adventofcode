import os
import argparse
from utils import readline_input_file

INPUT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                          'inputs/crabs_horizontal_position')


def get_fuel_cost_part1(x1, x2):
    """Get the fuel that would cost move from x1 to x2, when each step has cost 1."""
    return abs(x1-x2)


def get_fuel_cost_part2(x1, x2):
    """Get the fuel that would cost move from x1 to x2, when:

    Moving from each change of 1 step in horizontal position costs 1 more unit of fuel than the last. This can be easily
    computed as a triangular number/binomial coefficient.
    """
    steps = abs(x1-x2)
    return steps*(steps+1)/2


def get_total_fuel(fuel_list):
    """Get the fuel that the submarine would spent."""
    total = 0

    for fuel_i in fuel_list:
        total += fuel_i

    return total


def main():
    horizontal_positions = []

    for number in readline_input_file(INPUT_PATH).split(','):
        horizontal_positions.append(int(number))

    initial = min(horizontal_positions)
    current_pos = initial
    max_pos = max(horizontal_positions)
    fuel_part1 = [0]*len(horizontal_positions)
    fuel_part2 = [0]*len(horizontal_positions)
    total_fuel_part1 = 0
    total_fuel_part2 = 0
    min_fuel_part1 = 999999
    min_fuel_part2 = 9999999999

    while current_pos < max_pos:
        for i in range(len(horizontal_positions)):
            fuel_part1[i] = get_fuel_cost_part1(horizontal_positions[i], current_pos)
            fuel_part2[i] = get_fuel_cost_part2(horizontal_positions[i], current_pos)

        total_fuel_part1, total_fuel_part2 = get_total_fuel(fuel_part1), get_total_fuel(fuel_part2)
        min_fuel_part1 = total_fuel_part1 if total_fuel_part1 < min_fuel_part1 else min_fuel_part1
        min_fuel_part2 = total_fuel_part2 if total_fuel_part2 < min_fuel_part2 else min_fuel_part2
        current_pos += 1

    print(f"Min fuel when each step has cost 1: {min_fuel_part1}")
    print(f"Min fuel when each step costs 1 more unit of fuel than the last: {min_fuel_part2}")


if __name__ == '__main__':
    main()
