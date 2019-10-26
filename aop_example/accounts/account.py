from aop_example.decorators import logged


class Account:
    def __init__(self, id, balance):
        self.__id = id
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance

    @logged
    def withdraw(self, amount):
        self.__balance -= amount

    @logged
    def deposit(self, amount):
        self.__balance += amount

    def __repr__(self):
        return f"A/C {self.__id}"