from data_base import DataBase
from schemas import AccountCreate
from pydantic import ValidationError

def main():
    database = DataBase()
    print("Enter the details for Account you want to add.")
    while True:
        choice = int(input("0.Add account \n1.quit\nchoice: "))
        if choice != 1:
            acc_num = input("Account number: ")
            name = input("User name: ")
            pin = input("4 digit pin: ")
            balance = input("initial balance: ")
            try:
                account = AccountCreate(account_number=acc_num, name=name, pin=pin, balance=balance)
            except ValidationError as e:
                print(f"[Error] {e}")
                continue
            database.add_account(account.account_number, account.name, account.pin, account.balance)
            print(f"Account added for {name} in bank.")
            continue
        else:
            print("Quit.")
            break

if __name__=="__main__":
    main()