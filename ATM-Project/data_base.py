import sqlite3
from exceptions import AccountNotFoundError
from utils import hash_pin

class DataBase:
    def __init__(self,database="data/bank.db"):
        self.database_path = database
        self.connection = sqlite3.connect(database)
        
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        
        command = """
        CREATE TABLE IF NOT EXISTS account(
            account_number TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            balance REAL NOT NULL DEFAULT 0.0,
            pin_hash TEXT NOT NULL,
            failed_attempts INTEGER NOT NULL DEFAULT 0,
            is_locked INTEGER NOT NULL DEFAULT 0
        )
        """
        self.cursor.execute(command)
        self.connection.commit()

    def get_account_data(self, account_number):
            acc_num = str(account_number)
            self.cursor.execute("SELECT * FROM account WHERE account_number = ?", (acc_num, ))
            row = self.cursor.fetchone()
            if row is None:
                raise AccountNotFoundError("Account number not in database.")
            return row

    def account_exist(self, account_number) -> bool:
        acc_num = str(account_number)
        self.cursor.execute("SELECT 1 FROM account WHERE account_number=?",(acc_num,))
        row = self.cursor.fetchone()
        
        return row is not None
    
    def add_account(self, account_number, name, pin_hash, balance=0.0):
        acc_num = str(account_number)
        pin_hash = hash_pin(pin_hash)
        
        insert_query = """
        INSERT INTO account (account_number, name, balance, pin_hash, failed_attempts, is_locked)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        
        self.cursor.execute(insert_query, (acc_num, name, float(balance), pin_hash, 0, 0))
        
        self.connection.commit() 

    def update_balance(self,acc_number,new_balance):
        acc_num = str(acc_number)  
        self.cursor.execute(
            "UPDATE account SET balance=? WHERE account_number=?",
            (float(new_balance),acc_num)
        )
        if self.cursor.rowcount == 0:
            raise AccountNotFoundError("Account number not in database.")
        self.connection.commit()
        
        print(f"Success! Balance for account {acc_num} updated to {new_balance}.")

    def update_failed_attempts(self, account_number, failed_attempts, is_locked):
        acc_num = str(account_number)
        self.cursor.execute(
            "UPDATE account SET failed_attempts=?, is_locked=? WHERE account_number=?",
            (int(failed_attempts),int(is_locked),acc_num)
        )
        if self.cursor.rowcount == 0:
            raise AccountNotFoundError("Account number not in database.")
        self.connection.commit()  

    def __del__(self):
         if hasattr(self, 'connection'):
              self.connection.close()