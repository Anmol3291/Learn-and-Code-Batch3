class ATMException(Exception):
    pass

class InsufficientFundsException(ATMException):
    pass

class InvalidPinException(ATMException):
    pass

class DailyLimitExceededException(ATMException):
    pass

class ATMOutOfCashException(ATMException):
    pass

class ServerConnectionError(ATMException):
    pass
