from aop_example.decorators import logged, throttled


@throttled(100)
@logged
def transfer(fromAccount, toAccount, amount):
    fromAccount.withdraw(amount)
    toAccount.deposit(amount)