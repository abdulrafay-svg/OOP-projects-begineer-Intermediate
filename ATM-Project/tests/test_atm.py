import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from data_base import DataBase
from logger import TransactionLogger
from atm import ATM
from utils import hash_pin


@pytest.fixture
def atm_with_one_account():
    db_path, ledger_path = "test_users.csv", "test_ledger.csv"
    db = DataBase(database=db_path)
    db.add_account("321", "Ahraaf", "6541", 2000.0)
    logger = TransactionLogger(ledger_path=ledger_path)
    atm = ATM(db, logger)
    yield atm
    for f in (db_path, ledger_path):
        if os.path.exists(f):
            os.remove(f)


def test_successful_login_and_deposit(monkeypatch, atm_with_one_account):
    # simulate: account number -> correct pin -> deposit 500 -> logout -> quit
    inputs = iter(["321", "6541", "2", "500", "4", "q"])
    monkeypatch.setattr("builtins.input", lambda _="": next(inputs))

    atm_with_one_account.run_atm()

    updated_row = atm_with_one_account.db.get_account_data("321")
    assert updated_row["balance"] == 2500.0


def test_wrong_pin_increments_failed_attempts(monkeypatch, atm_with_one_account):
    inputs = iter(["321", "0000", "q"])
    monkeypatch.setattr("builtins.input", lambda _="": next(inputs))

    atm_with_one_account.run_atm()

    row = atm_with_one_account.db.get_account_data("321")
    assert row["failed_attempts"] == 1
    assert bool(row["is_locked"]) is False
