from os import read
import os
from utils import readline_input_file


INPUT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'inputs/lanternfish_ages_test')


class Lanternfish:
    def __init__(self, initial_internal_timer, fresh=False):
        self.internal_timer = int(initial_internal_timer)
        self.fresh = fresh

    def day_passed(self):
        self.internal_timer -= 1

    def set_new_timer(self, new_timer):
        self.internal_timer = new_timer
        self.fresh = True

    def can_create_new_lf(self):
        return True if self.internal_timer == 0 else False

    def can_pass_a_day(self):
        return not self.fresh

    def update_fresh(self):
        self.fresh = False

    def __repr__(self):
        return str(self.internal_timer)


class Shoal:
    def __init__(self, input_path):
        self.NEW_TIMER = 6
        self.INITIAL_TIMER = 8
        self.fishes = self.get_initial_shoal(self.get_initial_shoal_ages(input_path))

    def get_initial_shoal_ages(self, input_path):
        lanternfish_ages = readline_input_file(INPUT_PATH).split(',')
        lanternfish_ages[len(lanternfish_ages)-1] = lanternfish_ages[len(lanternfish_ages)-1].replace('\n', '')

        return lanternfish_ages

    def get_initial_shoal(self, lanternfish_ages):
        lanternfishes = []

        for age in lanternfish_ages:
            lanternfishes.append(Lanternfish(age))

        return lanternfishes

    def add_new_fish(self):
        self.fishes.append(Lanternfish(self.INITIAL_TIMER, fresh=True))

    def pass_x_days(self, n_days):
        for _ in range(n_days):
            for fish in self.fishes:
                if fish.can_create_new_lf():
                    fish.set_new_timer(self.NEW_TIMER)
                    self.add_new_fish()

                if fish.can_pass_a_day():
                    fish.day_passed()
                else:
                    fish.update_fresh()

            # print(f"After {_+1} days: {self.fishes}")

    def __repr__(self):
        return '[' + ', '.join(map(str, self.fishes)) + ']'


def main():
    DAYS_TO_PASS = 18
    input_shoal = Shoal(INPUT_PATH)
    print(f"Initial fish number: {len(input_shoal.fishes)}")
    # print(f"Initial state: {input_shoal.fishes}")
    input_shoal.pass_x_days(DAYS_TO_PASS)
    print(f"Fish number after {DAYS_TO_PASS} days: {len(input_shoal.fishes)}")


if __name__ == '__main__':
    main()
