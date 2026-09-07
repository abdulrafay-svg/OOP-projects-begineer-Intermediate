from pydantic import BaseModel,Field

class AccountCreate(BaseModel):
    account_number : str = Field(pattern=r'^\d{10}$')
    name: str
    pin: str = Field(pattern=r'^\d{4}$')
    balance: float = 0.0 

class TransactionRequest(BaseModel):
    amount : float

class PinCheck(BaseModel):
    pin: str