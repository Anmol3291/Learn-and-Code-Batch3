# Assignment 1: The below program is to Roll the Dice

import random


def fun(s):
    n = random.randint(1, s)
    return n


def main():
    s = 6
    r1 = True
    while r1:
        r2 = input("Ready to roll? Enter Q to Quit")
        if r2.lower() != "q":
            n = fun(s)
            print("You have rolled a", n)
        else:
            r1 = False


# Solution


def getSideValue(total_sides_on_dice):
    get_random_side_value = random.randint(1, total_sides_on_dice)
    return get_random_side_value


def main():
    total_sides_on_dice = 6
    want_to_roll = True
    while want_to_roll:
        user_input = input("Ready to roll? Enter Q to Quit")
        if user_input.lower() != "q":
            rolled_value = getSideValue(total_sides_on_dice)
            print("You have rolled a", rolled_value)
        else:
            want_to_roll = False
