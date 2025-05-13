from models.atm import ATM
from models.account import Account
from services.atm_operation import ATMOperation

if __name__ == "__main__":
    atm = ATM(cash_available=5000)
    account = Account(
        account_number="1234567890", pin=1234, balance=4000, daily_limit=3000
    )
    atm_operation = ATMOperation(atm, account)

    atm_operation.withdraw_from_atm(1111, 500)
    atm_operation.withdraw_from_atm(2222, 500)
    atm_operation.withdraw_from_atm(1234, 500)
    atm_operation.withdraw_from_atm(3333, 500)
    atm_operation.withdraw_from_atm(4567, 500)
    atm_operation.withdraw_from_atm(4987, 500)
