# transaction.py

class Transaction:
    def __init__(self, customer_name):
        self.customer_name = customer_name

    def display(self):
        pass


class Deposit(Transaction):
    def __init__(self, customer_name, amount):
        super().__init__(customer_name)
        self.amount = amount

    def display(self):
        print(f"Deposit: {self.customer_name} - Amount: ${self.amount}")


class Withdraw(Transaction):
    def __init__(self, customer_name, amount):
        super().__init__(customer_name)
        self.amount = amount

    def display(self):
        print(f"Withdraw: {self.customer_name} - Amount: ${self.amount}")


class Check(Transaction):
    def __init__(self, customer_name):
        super().__init__(customer_name)

    def display(self):
        print(f"Check: {self.customer_name}")


class Bet(Transaction):
    def __init__(self, customer_name, amount, market, side):
        super().__init__(customer_name)
        self.amount = amount
        self.market = market
        self.side = side

    def display(self):
        print(f"Bet: {self.customer_name} - Amount: ${self.amount} - Market: {self.market} - Side: {self.side}")
