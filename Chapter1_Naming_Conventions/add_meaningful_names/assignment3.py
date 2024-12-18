# Assignment 3: The below program is to check whether the number is Armstrong number or not


def is_armstrong_number(number):
    # Initializing sum and number of digits
    sum_of_powers = 0
    num_of_digits = 0

    # Calculating number of individual digits
    temp_number = number
    while temp_number > 0:
        num_of_digits += 1
        temp_number //= 10

    # Finding Armstrong number
    temp_number = number
    while temp_number > 0:
        digit = temp_number % 10
        sum_of_powers += digit**num_of_digits
        temp_number //= 10
    return sum_of_powers


# End of function

# User input
user_input_number = int(input("\nPlease enter the number to check for Armstrong: "))

if user_input_number == is_armstrong_number(user_input_number):
    print(f"\n{user_input_number} is an Armstrong number.\n")
else:
    print(f"\n{user_input_number} is not an Armstrong number.\n")
