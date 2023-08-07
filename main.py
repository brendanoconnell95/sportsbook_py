import csv
from transaction import Deposit, Withdraw, Check, Bet
from sportsbook import Sportsbook

def read_transactions_from_csv(csv_file):
    transactions = []
    with open(csv_file, mode="r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            customer_name = row["Name"]
            event_type = row["Type"]
            amount = float(row["Amount"]) if row["Amount"] else 0
            market = row["Market"] if "Market" in row else ""
            side = row["Side"] if "Side" in row else ""

            if event_type == "Deposit":
                transactions.append(Deposit(customer_name, amount))
            elif event_type == "Withdraw":
                transactions.append(Withdraw(customer_name, amount))
            elif event_type == "Check":
                transactions.append(Check(customer_name))
            elif event_type == "Bet":
                transactions.append(Bet(customer_name, amount, market, side))

    return transactions

if __name__ == "__main__":
    sportsbook = Sportsbook()

    # Reset all account balances to 0
    sportsbook.reset_account_balances()

    # Delete all bets from the bets table
    sportsbook.delete_all_bets()

    # Read transactions from CSV and process them
    transactions = read_transactions_from_csv("events.csv")
    sportsbook.process_transactions(transactions)

    # Print account balances for all customers
    sportsbook.print_account_balances()

    # Print all bets for each customer with status "pending"
    customers = sportsbook.get_all_customers()
    for customer in customers:
        sportsbook.print_customer_bets(customer, status="pending")

    sportsbook.settle_market("A","home")

    # Print account balances for all customers
    sportsbook.print_account_balances()

    # Print all bets for each customer with status "all"
    customers = sportsbook.get_all_customers()
    for customer in customers:
        sportsbook.print_customer_bets(customer, status="all")

    sportsbook.close()

