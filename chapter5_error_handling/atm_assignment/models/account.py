from exceptions.atm_exceptions import (
    InsufficientFundsException,
    InvalidPinException,
    DailyLimitExceededException,
)


class Account:
    def __init__(self, account_number, pin, balance, daily_limit):
        self.account_number = account_number
        self.pin = pin
        self.balance = balance
        self.daily_limit = daily_limit
        self.daily_withdrawn = 0
        self.invalid_pin_attempts = 0
        self.is_blocked = False

    def validate_pin(self, input_pin):
        if self.is_blocked:
            raise InvalidPinException(
                "Card is blocked due to multiple invalid attempts."
            )
        if input_pin != self.pin:
            self.invalid_pin_attempts += 1
            if self.invalid_pin_attempts >= 3:
                self.is_blocked = True
                raise InvalidPinException("Card blocked after 3 invalid pin attempts.")
            raise InvalidPinException("Invalid PIN")
        self.invalid_pin_attempts = 0

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsException("Insufficient account balance.")
        if self.daily_withdrawn + amount > self.daily_limit:
            raise DailyLimitExceededException("Daily withdrawal limit exceeded.")
        self.balance -= amount
        self.daily_withdrawn += amount
