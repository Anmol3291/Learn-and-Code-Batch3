# Assignment 2: The below program is to guess the correct number between 1 to 100

import random


def fun(s):
    if s.isdigit() and 1 <= int(s) <= 100:
        return True
    else:
        return False


def main():
    n = random.randint(1, 100)
    gn = False
    g = input("Guess a number between 1 and 100:")
    ng = 0
    while not gn:
        if not fun(g):
            g = input("I wont count this one Please enter a number between 1 to 100")
            continue
        else:
            ng += 1
            g = int(g)

        if g < n:
            g = input("Too low. Guess again")
        elif g > n:
            g = input("Too High. Guess again")
        else:
            print("You guessed it in", ng, "guesses!")
            gn = True


main()

# Solution


def validateEnteredNumber(guessed_number):
    if guessed_number.isdigit() and 1 <= int(guessed_number) <= 100:
        return True
    else:
        return False


def main():
    random_number = random.randint(1, 100)
    is_guessed = False
    guessed_number = input("Guess a number between 1 and 100:")
    number_of_guesses = 0
    while not is_guessed:
        if not validateEnteredNumber(guessed_number):
            guessed_number = input(
                "I wont count this one Please enter a number between 1 to 100"
            )
            continue
        else:
            number_of_guesses += 1
            guessed_number = int(guessed_number)

        if guessed_number < random_number:
            guessed_number = input("Too low. Guess again")
        elif guessed_number > random_number:
            guessed_number = input("Too High. Guess again")
        else:
            print("You guessed it in", number_of_guesses, "guesses!")
            is_guessed = True


main()
