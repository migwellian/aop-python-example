from aop_example.decorators import logged


@logged
def transfer(fromAccount, toAccount, amount):
    fromAccount.withdraw(amount)
    toAccount.deposit(amount)