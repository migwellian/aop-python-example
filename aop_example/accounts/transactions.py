from aop_example.decorators import logged, throttled, access_controlled, atomic


@throttled(100)
@logged
@access_controlled
@atomic
def transfer(fromAccount, toAccount, amount):
    fromAccount.withdraw(amount)
    toAccount.deposit(amount)