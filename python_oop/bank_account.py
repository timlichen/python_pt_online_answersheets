class BankAccount:
    def __init__(self, int_rate, balance):
        self.int_rate = int_rate
        self.balance = balance
    def deposit(self, amount):
        self.balance += amount
        return self
    def withdraw(self, amount):
        self.balance -= amount
        return self
    def display_account_info(self):
        print(self.balance)
        return self
    def yield_interest(self):
        interest = self.balance * self.int_rate
        self.balance += interest
        return self

account1 = BankAccount(.5, 0)
account2 = BankAccount(.5, 0)

account1.deposit(1).deposit(1).deposit(1).withdraw(2).yield_interest().display_account_info()

account2.deposit(1).deposit(1).withdraw(.25).withdraw(.25).withdraw(.25).withdraw(.25).yield_interest().display_account_info()