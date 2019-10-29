from aop_example.decorators import logged, database_backed


@database_backed
class Account:
    def __init__(self, id, balance):
        self.__id = id
        self.__balance = balance
        self.__is_active = True

    @property
    def balance(self):
        return self.__balance

    @logged
    def withdraw(self, amount):
        if not self.__is_active:
            raise Exception(f"Account {self.__id} is inactive: cannot withdraw funds")
        self.__balance -= amount

    @logged
    def deposit(self, amount):
        if not self.__is_active:
            raise Exception(f"Account {self.__id} is inactive: cannot deposit funds")
        self.__balance += amount

    def __repr__(self):
        return f"A/C {self.__id}"

    def freeze(self):
        self.__is_active = False

