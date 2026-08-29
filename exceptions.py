'''Making Exception classes in exception.py,
   so everyone can acces them from one location rather 
    than calling each other or making their own '''

class BankTransactionError(Exception): 
    '''creating base class that will catch any python exception'''
    pass
class AccountNotFoundError(BankTransactionError): pass
class InsufficientFundsError(BankTransactionError): pass
class AccountLockedError(BankTransactionError): pass
class InvalidAmountError(BankTransactionError): pass
class InvalidPinError(BankTransactionError): pass
