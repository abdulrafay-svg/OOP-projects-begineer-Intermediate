import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from data_base import DataBase
from exceptions import AccountNotFoundError

@pytest.fixture
def mock_db():
    test_db_file = "test_bank.db"
    if os.path.exists(test_db_file):
        os.remove(test_db_file)
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

def test_get_account_data(mock_db):
    account_info = mock_db.get_account_data("321")
    assert account_info["name"] == "Ahraaf"
    assert account_info["balance"] == 2000.0
    assert account_info["pin_hash"] == "6541"


def test_no_account(mock_db):
    with pytest.raises(AccountNotFoundError) as exc_info:
        mock_db.get_account_data("432")
    assert str(exc_info.value) == "Account number not in database."


def test_update_balance_persists(mock_db):
    mock_db.update_balance("321", 3500.0)
    reloaded = DataBase(database=mock_db.database_path)
    assert reloaded.get_account_data("321")["balance"] == 3500.0
    reloaded.connection.close()

def test_add_account(mock_db):
    mock_db.add_account("999", "Sara", "hashedpin", 100.0)
    row = mock_db.get_account_data("999")
    assert row["name"] == "Sara"
    assert row["balance"] == 100.0
