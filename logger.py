import os
from datetime import datetime
import pandas as pd

LEDGER_COLUMNS = ["timestamp", "account_number", "type", "amount", "status"]


class TransactionLogger:
    def __init__(self, ledger_path="data/ledger.csv"):
        self.ledger_path = ledger_path
        if not os.path.exists(ledger_path):
            os.makedirs(os.path.dirname(ledger_path) or ".", exist_ok=True)
            pd.DataFrame(columns=LEDGER_COLUMNS).to_csv(ledger_path, index=False)

    def log_transaction(self, account_number, transaction_type, amount, status):
        row = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "account_number": str(account_number),
            "type": transaction_type,
            "amount": amount,
            "status": status,
        }
        # append without loading the whole file into memory each time
        pd.DataFrame([row]).to_csv(
            self.ledger_path, mode="a", header=False, index=False
        )