# Assignment 2: The below program is to guess the correct number between 1 to 100
import random


def is_valid_guess(guess):
    return guess.isdigit() and 1 <= int(guess) <= 100


def main():
    target_number = random.randint(1, 100)
    has_guessed_correctly = False
    user_guess = input("Guess a number between 1 and 100: ")
    guess_count = 0

    while not has_guessed_correctly:
        if not is_valid_guess(user_guess):
            user_guess = input(
                "I won't count this one. Please enter a number between 1 and 100: "
            )
            continue
        else:
            guess_count += 1
            user_guess = int(user_guess)

        if user_guess < target_number:
            user_guess = input("Too low. Guess again: ")
        elif user_guess > target_number:
            user_guess = input("Too high. Guess again: ")
        else:
            print(f"You guessed it in {guess_count} guesses!")
            has_guessed_correctly = True


main()
