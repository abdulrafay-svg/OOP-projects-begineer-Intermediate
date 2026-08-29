"""
DataBase hands ATM a row -> ATM builds a BankAccount from that row ->
BankAccount enforces the rules -> ATM writes the updated numbers back
through DataBase.
"""
from exceptions import InsufficientFundsError, InvalidAmountError
from utils import hash_pin

class BankAccount:
    no_of_users = 0
    withdrawal_tax = 1.01
    def __init__(
        self,
        owner : str,
        balance : float = 0.0,
        account_number: str = None,
        pin_hash: str = None,
        failed_attempts: int = 0,
        is_locked: bool = False,
    ):
        self.owner = owner
        self.account_number = account_number
        self.__balance = balance
        self.__pin_hash = pin_hash
        self.failed_attempts = failed_attempts
        self.is_locked = is_locked
        BankAccount.no_of_users += 1
        
    def get_owner(self):
        return f"owner: {self.owner} "

    def get_balance(self):
        return f"Account Balance: {self.__balance}"

    def get_pin(self):
        return (self.__pin_hash)

    @property
    def balance(self):
        return self.__balance
    
    def add_amount(self,amount):
        if amount > 0:
            self.__balance += amount
        else:
            raise InvalidAmountError("Amount must be greater than 0.")

    def withdraw(self,amount):
        if amount <= 0 :
            raise InvalidAmountError("Amount can't be negative! ")
        total_cost = amount*self.withdrawal_tax
        if total_cost > self.__balance:
            raise InsufficientFundsError(f"You only have {self.__balance} but entered withdraw amount is {amount}")
        else:
            self.__balance -= total_cost

    def pin_check(self, pin):
        pin = str(pin)
        pin_hash = hash_pin(raw_pin= pin)
        return pin_hash == self.get_pin()

    def register_failed_attempt(self, max_attempts: int = 3):
        self.failed_attempts += 1
        if self.failed_attempts >= max_attempts :
            self.is_locked = True

    def reset_failed_attempts(self):
        self.failed_attempts = 0

    @classmethod
    def from_row(cls, row):
        """
        Build a BankAccount from a pandas Series (one row of users.csv).
        This is the ONLY place account.py knows a CSV/DataFrame exists,
        and even here it just reads plain values off the row.
        """
        return cls(
            owner=row["name"],
            balance=row["balance"],
            account_number=row.name,  # index value = account_number
            pin_hash=row["pin_hash"],
            failed_attempts=row["failed_attempts"],
            is_locked=bool(row["is_locked"]),
        )