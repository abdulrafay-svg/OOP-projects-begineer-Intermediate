from fastapi.testclient import TestClient
from api import app, db as api_db
import pytest
import sqlite3

# Import your real helper function to hash the password properly
from utils import hash_pin

client = TestClient(app)

@pytest.fixture
def mock_db():
    # Uses pure RAM memory to keep your data folder completely clean
    api_db.connection = sqlite3.connect(":memory:", check_same_thread=False)
    api_db.connection.row_factory = sqlite3.Row
    api_db.cursor = api_db.connection.cursor()
    
    api_db.cursor.execute("""
    CREATE TABLE IF NOT EXISTS account (
        account_number TEXT PRIMARY KEY,
        name TEXT,
        balance REAL,
        pin_hash TEXT,
        failed_attempts INTEGER,
        is_locked INTEGER
    )""")
    api_db.cursor.execute("DELETE FROM account")
    
    # FIX: Hash the raw pin "3333" exactly how your code expects it in production!
    secure_hash = hash_pin(raw_pin="3333")
    
    insert_query = """
    INSERT INTO account(account_number, name, balance, pin_hash, failed_attempts, is_locked)
    VALUES(?, ?, ?, ?, ?, ?)"""
    api_db.connection.execute(insert_query, ("321", "Rafay", 20000.0, secure_hash, 0, 0))
    api_db.connection.commit()
    
    yield 
    api_db.connection.close()


# === 1. BALANCE ENDPOINT TESTS ===

def test_get_balance_success(mock_db):
    response = client.get("/account/321/balance")
    assert response.status_code == 200
    assert response.json() == {"account_number": "321", "balance": 20000.0}

def test_get_balance_not_found(mock_db):
    response = client.get("/account/999/balance")
    assert response.status_code == 404
    assert response.json()["detail"] == "Account not Found!"


# === 2. WITHDRAW ENDPOINT TESTS ===

def test_withdraw_success(mock_db):
    # Base balance is 20000.0. Tax is 1.01.
    # 5000 * 1.01 = 5050.0 total cost. New balance should be 20000 - 5050 = 14950.0
    response = client.post("/account/321/withdraw", json={"amount": 5000.0})
    assert response.status_code == 200
    assert response.json() == {
        "status": "success", 
        "account_number": "321", 
        "new_balance": 14950.0
    }

def test_withdraw_insufficient_funds(mock_db):
    response = client.post("/account/321/withdraw", json={"amount": 30000.0})
    assert response.status_code == 400
    assert response.json()["detail"] == "You have 20000.0 in your account."


# === 3. DEPOSIT ENDPOINT TESTS ===

def test_deposit_success(mock_db):
    response = client.post("/account/321/deposit", json={"amount": 5000.0})
    assert response.status_code == 200
    assert response.json() == {
        "status": "success", 
        "account_number": "321", 
        "new_balance": 25000.0
    }

def test_deposit_invalid_amount(mock_db):
    response = client.post("/account/321/deposit", json={"amount": -100.0})
    assert response.status_code == 400
    assert response.json()["detail"] == "Amount must be positive number."


# === 4. LOGIN ENDPOINT TESTS ===

def test_login_success(mock_db):
    response = client.post("/account/321/login", json={"pin": "3333"})
    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "Authentication successful"}

def test_login_wrong_pin(mock_db):
    response = client.post("/account/321/login", json={"pin": "1234"})
    assert response.status_code == 401
    assert "Incorrect pin" in response.json()["detail"]

def test_login_locked_after_3_attempts(mock_db):
    api_db.connection.execute("UPDATE account SET failed_attempts = 2 WHERE account_number = '321'")
    api_db.connection.commit()
    
    response = client.post("/account/321/login", json={"pin": "1234"})
    assert response.status_code == 401
    assert "Too many incorect attempts , account is locked!" in response.json()["detail"]
