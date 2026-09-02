from data_base import DataBase
from logger import TransactionLogger
from atm import ATM


def main():
    db = DataBase("data/bank.db")
    logger = TransactionLogger("data/ledger.csv")
    atm = ATM(db, logger)
    atm.run_atm()


if __name__ == "__main__":
    main()