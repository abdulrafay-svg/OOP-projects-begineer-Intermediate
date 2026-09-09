# Rafay's Digital Bank

A CLI + REST API banking system with SQLite persistence, built from scratch in Python.

**Live API:** https://oop-projects-begineer-intermediate-production.up.railway.app

## What it does

Two interfaces on top of the same account logic:

- **CLI (`main.py`)** — login by account number + PIN, deposit, withdraw, check balance, view mini-statement. PIN lockout after failed attempts.
- **REST API (`api.py`)** — the same account operations exposed as HTTP endpoints via FastAPI, deployed on Railway.

Every transaction is written to `data/ledger.csv` as an append-only log, and account state (balance, PIN hash, lock status) lives in SQLite (`data/bank.db`).

## Architecture

```
Client (CLI or HTTP)
      |
   atm.py / api.py      <- orchestration layer
      |
  account.py             <- BankAccount: business rules (balance, PIN, lock logic)
      |
data_base.py             <- SQLite persistence
      |
 logger.py                <- CSV transaction ledger (pandas)
```

- `exceptions.py` — custom exception hierarchy (`BankTransactionError` base, with `AccountNotFoundError`, `InsufficientFundsError`, `AccountLockedError`, `InvalidAmountError`, `InvalidPinError`) so every layer raises and catches the same vocabulary instead of generic exceptions.
- `schemas.py` — Pydantic models (`AccountCreate`, `TransactionRequest`, `PinCheck`) validate all API input before it reaches account logic.
- `utils.py` — PIN hashing (SHA-256); raw PINs are never stored.
- `seed_users.py` — standalone script to add test accounts to the database.

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/account/{account_number}/balance` | Get current balance |
| POST | `/account/{account_number}/withdraw` | Withdraw an amount |
| POST | `/account/{account_number}/deposit` | Deposit an amount |

(All return 404 for an unknown account number, and the relevant 4xx for invalid/locked/insufficient-funds cases via the custom exception hierarchy.)

## Running locally

```bash
git clone <repo-url>
cd ATM-Project
pip install -e .

# CLI
python main.py

# API
uvicorn api:app --reload
```

## Testing

```bash
pytest
```
Covers `account.py`, `data_base.py`, `atm.py`, and the API layer (`tests/test_account.py`, `tests/test_database.py`, `tests/test_atm.py`, `tests/test_api.py`).

## Deployment

Deployed on Railway, running `uvicorn api:app --host 0.0.0.0 --port $PORT` (see `Procfile`). Python 3.13.

## Stack

Python · SQLite · FastAPI · Pydantic · pandas (ledger logging) · pytest · Railway

## Status

v1.0.0 — core account operations (deposit, withdraw, balance, PIN auth + lockout) complete and deployed. No ORM, no auth tokens, no currency conversion by design — kept intentionally scoped rather than gold-plated.
