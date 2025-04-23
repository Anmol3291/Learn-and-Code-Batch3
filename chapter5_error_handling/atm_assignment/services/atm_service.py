from abc import ABC, abstractmethod


class ATMService(ABC):
    @abstractmethod
    def withdraw_from_atm(self, pin: int, amount: int):
        pass
