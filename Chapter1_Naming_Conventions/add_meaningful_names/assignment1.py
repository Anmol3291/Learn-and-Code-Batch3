# Assignment 1: The below program is to Roll the Dice

import random


def roll_dice(sides):
    rolled_value = random.randint(1, sides)
    return rolled_value


def main():
    sides = 6
    start = True
    while start:
        user_input = input("Ready to roll? Enter Q to Quit")
        if user_input.lower() != "q":
            rolled_value = roll_dice(sides)
            print("You have rolled a", rolled_value)
        else:
            start = False


main()
