class User(object):
    def __init__(self):
        self.name = "Tom"
        self.email = "tom@email.com"
        self.account_balance = 0

    def make_deposit(self, amount):	
    	self.account_balance += amount
    
    def make_withdrawal(self, amount):
        self.account_balance -= amount
    
    def display_user_balance(self):
        print("User: {}, Balance: {}".format(self.name, self.account_balance))

    def transfer_money(self, other_user, amount):
        self.make_withdrawal(amount)
        other_user.make_deposit(amount)

user1 = User()
user2 = User()
user3 = User()

user1.make_deposit(10)
user1.make_deposit(20)
user1.make_deposit(30)
user1.make_withdrawal(5)
user1.display_user_balance()

user2.make_deposit(10)
user2.make_deposit(20)
user2.make_withdrawal(5)
user2.make_withdrawal(5)
user2.display_user_balance()

user3.make_deposit(3)
user3.make_withdrawal(1)
user3.make_withdrawal(1)
user3.make_withdrawal(1)
user3.display_user_balance()

user1.transfer_money(user3, 55)
user1.display_user_balance()
user3.display_user_balance()