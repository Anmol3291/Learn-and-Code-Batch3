# Assignment 3: The below program is to check whether the number is Armstrong number or not


def fun(N):
    # Initializing Sum and Number of Digits
    s = 0
    t = 0

    # Calculating Number of individual digits
    t2 = N
    while t2 > 0:
        t = t + 1
        t2 = t2 // 10

    # Finding Armstrong Number
    t2 = N
    for n in range(1, t2 + 1):
        R = t2 % 10
        s = s + (R**t)
        t2 //= 10
    return s


# End of Function

# User Input
N2 = int(input("\nPlease Enter the Number to Check for Armstrong: "))

if N2 == fun(N2):
    print("\n %d is Armstrong Number.\n" % N2)
else:
    print("\n %d is Not a Armstrong Number.\n" % N2)


# Solution


def calculateArmstrongValue(user_entered_number):
    armstrong_value = 0
    number_of_digits = 0

    temporary_number = user_entered_number
    while temporary_number > 0:
        number_of_digits = number_of_digits + 1
        temporary_number = temporary_number // 10

    temporary_number = user_entered_number
    for time in range(1, number_of_digits + 1):
        remainder = temporary_number % 10
        armstrong_value = armstrong_value + (remainder**number_of_digits)
        temporary_number //= 10

    return armstrong_value


user_entered_number = int(input("\nPlease Enter the Number to Check for Armstrong: "))
if user_entered_number == calculateArmstrongValue(user_entered_number):
    print("\n %d is Armstrong Number.\n" % user_entered_number)
else:
    print("\n %d is Not a Armstrong Number.\n" % user_entered_number)
