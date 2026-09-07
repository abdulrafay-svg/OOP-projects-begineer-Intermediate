import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from data_base import DataBase
import pytest
from account import BankAccount
from exceptions import InvalidAmountError, InsufficientFundsError

@pytest.fixture
def mock_db():
    test_db_file = "test_bank.db"
    db = DataBase(database=test_db_file)
    insert_query = """
    INSERT INTO account(account_number, name, balance, pin_hash, failed_attempts, is_locked)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    db.cursor.execute(insert_query,(321,"Ahraaf",2000.0,6541,0,0))
    db.connection.commit()
    yield db
    if hasattr(db, 'connection'):
        db.connection.close()
    if os.path.exists(test_db_file):
        try:
            os.remove(test_db_file)
        except PermissionError:
            pass

@pytest.fixture
def fresh_account():
    return BankAccount("Rafay", 1000.0)


def test_initial_balance(fresh_account):
    assert fresh_account.get_balance() == 1000.0


def test_increased_balance_after_deposit(fresh_account):
    fresh_account.add_amount(1000.0)
    assert fresh_account.get_balance() == 2000.0


def test_negative_deposit(fresh_account):
    with pytest.raises(InvalidAmountError) as exc_info:
        fresh_account.add_amount(-1000)
    assert str(exc_info.value) == "Amount must be greater than 0."


def test_greater_withdraw_amount(fresh_account):
    with pytest.raises(InsufficientFundsError) as ins:
        fresh_account.withdraw(3000.0)
    assert str(ins.value) == "You only have 1000.0 but entered withdraw amount is 3000.0"


def test_withdraw_record(fresh_account):
    # Fresh account starts at 1000.0. Tax is 200 * 1.01 = 202.0. Remaining = 798.0
    fresh_account.withdraw(200.0)
    assert fresh_account.get_balance() == 798.0


def test_pin_check():
    from utils import hash_pin
    acc = BankAccount("Rafay", 1000.0, pin_hash=hash_pin("1234"))
    assert acc.pin_check("1234") is True
    assert acc.pin_check("0000") is False

def test_from_row_roundtrip(mock_db):        # add mock_db as a parameter
    mock_db.cursor.execute("SELECT * FROM account WHERE account_number = ?", (321, ))
    row = mock_db.cursor.fetchone()
    acc = BankAccount.from_row(row)
    assert acc.account_number == "321"
    assert acc.owner == "Ahraaf"
    assert acc.balance == 2000.0


