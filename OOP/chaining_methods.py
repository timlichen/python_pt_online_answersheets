class User(object):
    def __init__(self):
        self.name = "Tom"
        self.email = "tom@email.com"
        self.account_balance = 0

    def make_deposit(self, amount):	
        self.account_balance += amount
        return self
    
    def make_withdrawal(self, amount):
        self.account_balance -= amount
        return self
    def display_user_balance(self):
        print("User: {}, Balance: {}".format(self.name, self.account_balance))
        return self

    def transfer_money(self, other_user, amount):
        self.make_withdrawal(amount)
        other_user.make_deposit(amount)
        return self

user1 = User()
user2 = User()
user3 = User()

user1.make_deposit(10).make_deposit(20).make_deposit(30).make_withdrawal(5).display_user_balance()

user2.make_deposit(10).make_deposit(20).make_withdrawal(5).make_withdrawal(5).display_user_balance()

user3.make_deposit(3).make_withdrawal(1).make_withdrawal(1).make_withdrawal(1).display_user_balance()

user1.transfer_money(user3, 55).display_user_balance()
user3.display_user_balance()