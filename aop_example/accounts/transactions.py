from aop_example.decorators import logged, throttled, access_controlled


@throttled(100)
@logged
@access_controlled
def transfer(fromAccount, toAccount, amount):
    fromAccount.withdraw(amount)
    toAccount.deposit(amount)