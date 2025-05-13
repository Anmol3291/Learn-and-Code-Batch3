from exceptions.atm_exceptions import ATMOutOfCashException, ServerConnectionError


class ATM:
    def __init__(self, cash_available):
        self.cash_available = cash_available
        self.server_connected = True

    def check_server_connection(self):
        if not self.server_connected:
            raise ServerConnectionError("Unable to connect with server.")

    def withdraw_cash(self, account, pin, amount):
        self.check_server_connection()
        account.validate_pin(pin)
        if amount > self.cash_available:
            raise ATMOutOfCashException("ATM has insufficient cash.")
        account.withdraw(amount)
        self.cash_available -= amount
        return f"Withdrawal successful. Remaining balance: Rs. {account.balance} /-"
