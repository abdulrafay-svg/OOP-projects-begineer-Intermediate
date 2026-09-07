from fastapi import FastAPI,HTTPException
from data_base import DataBase
from exceptions import (AccountNotFoundError,
                        InsufficientFundsError,
                        InvalidAmountError,
                        AccountLockedError)
from schemas import TransactionRequest,PinCheck
from account import BankAccount

app = FastAPI()
db = DataBase()

@app.get("/account/{account_number}/balance")
def get_balance(account_number : str):
    try:
        row = db.get_account_data(account_number)
    except AccountNotFoundError:
        raise HTTPException(status_code=404, detail="Account not Found!")

    return {"account_number":row["account_number"], "balance": row["balance"]}

@app.post("/account/{account_number}/withdraw")
def withdraw(account_number : str , transaction : TransactionRequest):
    try:
        row = db.get_account_data(account_number)
    except AccountNotFoundError:
        raise HTTPException(status_code=404, detail="Account not Found! ")

    account = BankAccount.from_row(row)

    try:
        account.withdraw(transaction.amount)
        new_balance = account.balance    
    except InsufficientFundsError:
        raise HTTPException(status_code=400, detail=f"You have {row['balance']} in your account.")

    db.update_balance(account_number, new_balance)
    return {
        "status": "success", 
        "account_number": account_number, 
        "new_balance": new_balance
    }

@app.post("/account/{account_number}/deposit")
def deposit(account_number : str , transaction : TransactionRequest):
    try:
        row = db.get_account_data(account_number)
    except AccountNotFoundError:
        raise HTTPException(status_code=404, detail="Account not Found! ")

    account = BankAccount.from_row(row)

    try:
        account.add_amount(transaction.amount)   
        new_balance = account.balance
    except InvalidAmountError:
        raise HTTPException(status_code=400, detail=f"Amount must be positive number.")
    
    db.update_balance(account_number, new_balance)
    return {
        "status": "success", 
        "account_number": account_number, 
        "new_balance": new_balance
    }

@app.post("/account/{account_number}/login")
def pincheck(account_number : str, pin_check : PinCheck):
    try:
        row = db.get_account_data(account_number)
    except AccountNotFoundError:
        raise HTTPException(status_code=404, detail="Account not Found! ")

    account = BankAccount.from_row(row)
    if account.is_locked:
        raise HTTPException(status_code=403, detail="Account is locked!")
    
    if account.pin_check(pin_check.pin):
        account.reset_failed_attempts()
        db.update_failed_attempts(account_number,account.failed_attempts,account.is_locked)
        return {"status": "success", "message": "Authentication successful"}
    else:
        account.register_failed_attempt()
        db.update_failed_attempts(account_number,account.failed_attempts,account.is_locked)
        if account.failed_attempts == 3:
            raise HTTPException(status_code=401, detail="Too many incorect attempts , account is locked!")
        raise HTTPException(status_code=401, detail="Incorrect pin for Account!")