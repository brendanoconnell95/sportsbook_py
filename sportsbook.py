import sqlite3
from transaction import Transaction, Deposit, Withdraw, Check, Bet

class Sportsbook:
    def __init__(self):
        self.vigorish = 1.91
        self.connection = sqlite3.connect("bets.db")
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        # Create the bets table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS bets
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            customer_name TEXT,
                            amount REAL,
                            market TEXT,
                            side TEXT,
                            status TEXT)''')

        # Create the balances table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS balances
                            (customer_name TEXT PRIMARY KEY,
                            balance REAL)''')

        self.connection.commit()

    def update_balance(self, customer_name, amount):
        # Update the balance for a customer
        current_balance = self.get_account_balance(customer_name)
        new_balance = current_balance + amount
        self.cursor.execute("INSERT OR REPLACE INTO balances (customer_name, balance) VALUES (?, ?)", (customer_name, new_balance))
        self.connection.commit()
    
    def print_account_balances(self):
        # Print out the account balances for all customers
        self.cursor.execute("SELECT customer_name, balance FROM balances")
        print("Account Balances:")
        for row in self.cursor.fetchall():
            customer_name, balance = row
            print(f"{customer_name}: ${balance:.2f}")
        print()

    def get_all_customers(self):
        # Get all customers who have an account balance (even if it's 0)
        self.cursor.execute("SELECT DISTINCT customer_name FROM balances")
        customers = [row[0] for row in self.cursor.fetchall()]
        return customers

    def get_account_balance(self, customer_name):
        # Get the account balance for a customer
        self.cursor.execute("SELECT balance FROM balances WHERE customer_name=?", (customer_name,))
        row = self.cursor.fetchone()
        return row[0] if row else 0

    def record_bet(self, bet: Bet):
        self.update_balance(bet.customer_name, -bet.amount)  # Subtract the bet amount from the customer's balance
        self.cursor.execute('''INSERT INTO bets (customer_name, amount, market, side, status)
                            VALUES (?, ?, ?, ?, ?)''',
                            (bet.customer_name, bet.amount, bet.market, bet.side, bet.status))
        self.connection.commit()

    def print_customer_bets(self, customer_name, status="all"):
        # Print out all bets a customer has placed based on the specified status (pending, processed, or all)
        status_filter = ""
        if status.lower() in ("pending", "processed"):
            status_filter = f" AND status = '{status.lower()}'"

        query = f"SELECT id, amount, market, side, status FROM bets WHERE customer_name = ?{status_filter}"
        self.cursor.execute(query, (customer_name,))
        bets = self.cursor.fetchall()

        print(f"Bets for {customer_name} with status '{status.title()}':")
        for bet in bets:
            bet_id, amount, market, side, bet_status = bet
            print(f"Bet ID: {bet_id}, Amount: ${amount:.2f}, Market: {market}, Side: {side}, Status: {bet_status}")
        print()

    def process_transactions(self, transactions):
        for transaction in transactions:
            if isinstance(transaction, Deposit):
                self.update_balance(transaction.customer_name, transaction.amount)
            
            elif isinstance(transaction, Withdraw):
                account_balance = self.get_account_balance(transaction.customer_name)
                if account_balance >= transaction.amount:
                    self.update_balance(transaction.customer_name, -transaction.amount)
                else:
                    print(f"Insufficient balance for withdrawal: {transaction.customer_name}. "
                          f"Account Balance: ${account_balance:.2f}, Withdrawal Amount: ${transaction.amount:.2f}")
                    continue  # Skip processing this transaction
            
            elif isinstance(transaction, Bet):
                account_balance = self.get_account_balance(transaction.customer_name)
                if account_balance >= transaction.amount:
                    self.record_bet(transaction)
                else:
                    print(f"Insufficient balance for bet: {transaction.customer_name}. "
                          f"Account Balance: ${account_balance:.2f}, Bet Amount: ${transaction.amount:.2f}, Market: {transaction.market}, Side: {transaction.side}")
                    continue  # Skip processing this transaction
                    
            transaction.status = "processed"

    def settle_market(self, market, result):
        # Settle the bets in the given market based on the result (home or away)
        if result not in ("home", "away"):
            print("Invalid result. It should be 'home' or 'away'.")
            return

        market_bets = self.cursor.execute("SELECT * FROM bets WHERE market = ? AND status = 'pending'", (market,))
        for bet in market_bets:
            bet_id, customer_name, amount, _, side, bet_status = bet
            if side == result:
                amount_won = amount * self.vigorish
                self.update_balance(customer_name, amount_won)
                print(f"Bet ID: {bet_id}, Customer: {customer_name}, Amount Won: ${amount_won:.2f}")
                self.cursor.execute("UPDATE bets SET status = 'won' WHERE id = ?", (bet_id,))
            else:
                self.cursor.execute("UPDATE bets SET status = 'lost' WHERE id = ?", (bet_id,))

        self.connection.commit()

    def delete_all_bets(self):
        # Delete all bets from the bets table
        self.cursor.execute("DELETE FROM bets")
        self.connection.commit()

    def reset_account_balances(self):
        # Reset all account balances to 0 for all customers
        self.cursor.execute("UPDATE balances SET balance = 0")
        self.connection.commit()

    def close(self):
        self.connection.close()
