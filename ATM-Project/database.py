import pandas as pd
import os

from exceptions import AccountNotFoundError

COLUMNS = ["account_number", "name", "pin_hash", "balance", "failed_attempts", "is_locked"]
class DataBase:
    def __init__(self, database="data/users.csv"):
        self.database_path = database
        if not os.path.exists(database):
            os.makedirs(os.path.dirname(database) or ".", exist_ok=True)
            self.df = pd.DataFrame(columns=COLUMNS).set_index("account_number")
            self.df.index = self.df.index.astype(str)
            self.df["pin_hash"] = self.df["pin_hash"].astype(str)
            self.df.to_csv(database)
        else:
            self.df = pd.read_csv(
                database,
                index_col="account_number",
                dtype={"account_number": str, "pin_hash": str},
                skipinitialspace=True)
            self.df.index = self.df.index.astype(str)

    def get_account_data(self,account_number):
        acc_num = str(account_number)
        if acc_num in self.df.index:
            return self.df.loc[acc_num]
        else:
            raise AccountNotFoundError("Account number not in database.")

    def account_exist(self, account_number) -> bool:
        return str(account_number) in self.df.index

    def add_account(self, account_number, name, pin_hash, balance=0.0):
        acc_num = str(account_number)
        self.df.loc[acc_num]={
            "name" : name,
            "pin_hash" : pin_hash,
            "balance" : float(balance),
            "failed_attempts" : 0,
            "is_locked" : False,
        }
        self.save_database()

    def update_balance(self,acc_number,new_balance):
        acc_num = str(acc_number)  
        if acc_num in self.df.index:
            self.df.at[acc_num,"balance"] = float(new_balance)
            self.save_database()
            print(f"Success! Balance for account {acc_num} updated to {new_balance}.")
        else:
            raise AccountNotFoundError("Account number not found.")

    def update_failed_attempts(self, account_number, failed_attempts, is_locked):
        acc_num = str(account_number)
        if acc_num in self.df.index:
            self.df.at[acc_num,"failed_attempts"] = failed_attempts
            self.df.at[acc_num,"is_locked"] = bool(is_locked)
            self.save_database()
        else:
            raise AccountNotFoundError("Account number not found.")
            
    def save_database(self):
        self.df.to_csv(self.database_path)







