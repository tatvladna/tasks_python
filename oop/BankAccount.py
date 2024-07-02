class BalanceDescriptor:
    def __init__(self, overdraft=False):
        self.overdraft = overdraft

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        print('inside __get__')
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        print('inside __set__')
        if not isinstance(value, (int, float)):
            raise TypeError('incorrect type')

        if not self.overdraft:
            if value < 0:
                balance = instance.__dict__[self.name]
                raise ValueError(f'You can only withdraw {balance} dollars')
            instance.__dict__[self.name] = value
        else:
            pass


class BankAccount:
    balance = BalanceDescriptor()

    def __init__(self, acc_num, balance):
        self.account_number = acc_num
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount

    def get_balance(self):
        return self.balance



class SavingsAccount(BankAccount):
    ...


class CheckingAccount(BankAccount):
    balance = BalanceDescriptor(overdraft=True)

    def __init__(self, acc_num, balance, comission=0.5):
        super(CheckingAccount, self).__init__(acc_num, balance)
        self._comission = comission

    def deposit(self, amount):
        amount = amount * (1 - self._comission * 0.01)
        super().deposit(amount)

    def withdraw(self, amount):
        amount = amount * (1 + self._comission * 0.01)
        super().withdraw(amount)




b = BankAccount(123, 100)
b.deposit(200)
print(b.balance)
b.withdraw(50)
print(b.balance)

try:
    b.withdraw(300)
except Exception as e:
    print(e)

###################
print()

c = CheckingAccount(123, 100)
c.deposit(200)
print(c.balance)
c.withdraw(50)
print(c.balance)

try:
    c.withdraw(300)
except Exception as e:
    print(e)