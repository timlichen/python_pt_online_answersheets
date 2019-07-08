class User(object):
    def __init__(self):
        self.name = "Tom"
        self.email = "tom@email.com"
        self.account = {}
    def make_deposit(self, account_name, amount):
        self.account[account_name].deposit(amount)
        return self
    def make_withdrawl(self, account_name, amount):
        self.account[account_name].withdraw(amount)
        return self
    def display_user_balance(self, account_name):
        print("User: {}, Balance: {}".format(self.name, 
                                            self.account[account_name].balance))
    
    def add_bank_account(self, account_name, account_object):
        self.account[account_name] = account_object
        return self

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
user1 = User()
user1.add_bank_account('act_1', account1)
user1.make_deposit('act_1', 1).make_withdrawl('act_1', 1).display_user_balance('act_1')


