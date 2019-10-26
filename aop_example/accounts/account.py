class Account:
    def __init__(self, id, balance):
        self.__id = id
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance

    def withdraw(self, amount):
        self.__balance -= amount

    def deposit(self, amount):
        self.__balance += amount
        