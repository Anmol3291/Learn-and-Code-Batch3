from exceptions.atm_exceptions import ATMException
from services.atm_service import ATMService


class ATMOperation(ATMService):
    def __init__(self, atm, account):
        self.atm = atm
        self.account = account

    def withdraw_from_atm(self, pin: int, amount: int):
        try:
            message = self.atm.withdraw_cash(self.account, pin, amount)
            print(message)
        except ATMException as e:
            print(f"Transaction failed: {e}")
