from account import BankAccount
from database import DataBase
from logger import TransactionLogger
from exceptions import (
    AccountNotFoundError,
    AccountLockedError,
    InvalidPinError,
    BankTransactionError,
)

MAX_LOGIN_ATTEMPTS = 3


class ATM:
    def __init__(self, database: DataBase, logger: TransactionLogger, machine_cash: float = 50000.0):
        self.db = database
        self.logger = logger
        self.machine_cash = machine_cash
        self.current_account: BankAccount = None

    # ---------------- Phase 2: authentication ----------------
    def run_atm(self):
        print("=" * 30)
        print("      RAFAY'S DIGITAL BANK     ")
        print("=" * 30)
        while True:
            acc_num = input("\nEnter Account Number (or 'q' to quit): ").strip()
            if acc_num.lower() == "q":
                print("Goodbye!")
                break

            try:
                row = self.db.get_account_data(acc_num)
            except AccountNotFoundError:
                print("❌ Account not found. Try again.")
                continue

            account = BankAccount.from_row(row)

            if account.is_locked:
                print("❌ This account is locked due to too many failed PIN attempts.")
                self.logger.log_transaction(acc_num, "Login", 0, "LOCKED")
                continue

            pin = input("Enter 4-digit PIN: ").strip()
            if account.pin_check(pin):
                account.reset_failed_attempts()
                self.db.update_failed_attempts(acc_num, 0, False)
                self.current_account = account
                self.logger.log_transaction(acc_num, "Login", 0, "SUCCESS")
                self.main_menu()
            else:
                account.register_failed_attempt(MAX_LOGIN_ATTEMPTS)
                self.db.update_failed_attempts(acc_num, account.failed_attempts, account.is_locked)
                self.logger.log_transaction(acc_num, "Login", 0, "FAILED")
                if account.is_locked:
                    print("❌ Wrong PIN. Account is now LOCKED.")
                else:
                    remaining = MAX_LOGIN_ATTEMPTS - account.failed_attempts
                    print(f"❌ Wrong PIN. {remaining} attempt(s) left.")

     
    def main_menu(self):
        while self.current_account is not None:
            print("\n" + "-" * 30)
            print(f"Welcome, {self.current_account.owner}")
            print("1. Check Balance")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Logout")
            print("-" * 30)
            choice = input("Select an option (1-4): ").strip()

            if choice == "1":
                print(f"ℹ️  {self.current_account.get_balance()}")
            elif choice == "2":
                self.deposit()
            elif choice == "3":
                self.withdraw()
            elif choice == "4":
                self.logout()
            else:
                print("❌ Invalid choice! Please type a number between 1 and 4.")

    # ---------------- Phase 3a: deposit ----------------
    def deposit(self):
        acc_num = self.current_account.account_number
        try:
            amount = float(input("Amount to deposit: "))
            self.current_account.add_amount(amount)
            self.db.update_balance(acc_num, self.current_account.balance)
            self.logger.log_transaction(acc_num, "Deposit", amount, "SUCCESS")
            print(f"✅ {self.current_account.get_balance()}")
        except BankTransactionError as e:
            self.logger.log_transaction(acc_num, "Deposit", 0, "FAILED")
            print(f"❌ Transaction Denied! {e}")
        except ValueError:
            print("❌ Please enter a valid number.")

    # ---------------- Phase 3b: withdraw ----------------
    def withdraw(self):
        acc_num = self.current_account.account_number
        try:
            amount = float(input("Amount to withdraw: "))
            if amount > self.machine_cash:
                raise BankTransactionError("ATM does not have enough cash for this withdrawal.")

            self.current_account.withdraw(amount)
            self.db.update_balance(acc_num, self.current_account.balance)
            self.machine_cash -= amount
            self.logger.log_transaction(acc_num, "Withdrawal", amount, "SUCCESS")
            print(f"✅ {self.current_account.get_balance()}")
        except BankTransactionError as e:
            self.logger.log_transaction(acc_num, "Withdrawal", 0, "FAILED")
            print(f"❌ Transaction Denied! {e}")
        except ValueError:
            print("❌ Please enter a valid number.")

    # ---------------- Phase 4: logout ----------------
    def logout(self):
        print(f"Thank you, {self.current_account.owner}. Logging out.\n")
        self.current_account = None
