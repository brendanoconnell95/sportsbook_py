# main.py
from transaction import Transaction, Deposit, Withdraw, Check

def main():
    transactions = []

    # Sample transactions
    deposit_1 = Deposit("John Doe", 100)
    deposit_2 = Deposit("Alice Smith", 50)
    withdraw_1 = Withdraw("John Doe", 30)
    check_1 = Check("Alice Smith")

    transactions.extend([deposit_1, deposit_2, withdraw_1, check_1])

    # Display all transactions
    for transaction in transactions:
        transaction.display()


if __name__ == "__main__":
    main()
