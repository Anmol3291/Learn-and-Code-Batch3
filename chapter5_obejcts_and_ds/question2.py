"""
Customer
    - firstName: str
    - lastName: str
    - myWallet: Wallet

    - getFirstName(): str
    - getLastName(): str
    - getWallet(): Wallet    

    
Wallet
    - value: float

    - getTotalMoney(): float
    - setTotalMoney(value: float): None
    - addMoney(deposit: float): None
    - subtractMoney(debit: float): None

    


Client's Code


DeliveryBoy
    - variables ...

    - someMethod()
        payment = 2.00
        theWallet = myCustomer.getWallet()
        if(theWallet.getTotalMoney() > payment):
            theWallet.subtractMoney(payment)
        else:
            come back later and get my money.
        
"""


"""
Problem I can see:

here Customer Class gives direct access to it's wallet through getWallet() method, which is allowing external class (deliveryBoy) to modify the wallet directly.
it means any external class can add, subtract or even replace the Wallet without Customer knowing.
delivery boy is making decisions on behalf of customer, which is not good. best way he/she request payment from customer and customer can handle.

"""


"""
Here is modified version of the code:
Now Wallet is no longer accessible to external classes.
Customer handles it own payments and deposits.
"""


class Wallet:
    def __init__(self, initial_amount: float = 0.0):
        self.__balance = initial_amount

    def get_total_money(self) -> float:
        return self.__balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.__balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.__balance:
            raise ValueError("Insufficient balance.")
        self.__balance -= amount



class Customer:
    def __init__(self, first_name: str, last_name: str, initial_balance: float = 0.0):
        self.__first_name = first_name
        self.__last_name = last_name
        self.__wallet = Wallet(initial_balance)

    def get_first_name(self) -> str:
        return self.__first_name

    def get_last_name(self) -> str:
        return self.__last_name

    def make_payment(self, amount: float) -> bool:
        try:
            self.__wallet.withdraw(amount)
            return True
        except ValueError as e:
            print(f"Payment failed: {e}")
            return False

    def receive_money(self, amount: float) -> None:
        try:
            self.__wallet.deposit(amount)
        except ValueError as e:
            print(f"Deposit failed: {e}")

    def check_balance(self) -> float:
        return self.__wallet.get_total_money()


# Client's Code : for example

my_customer = Customer("Ravi", "Kumar", 10.0)
payment = 2.0

if my_customer.make_payment(payment):
    print("Payment received!")
else:
    print("Come back later and get my money.")

