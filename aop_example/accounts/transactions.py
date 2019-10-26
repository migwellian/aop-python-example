

def transfer(fromAccount, toAccount, amount):
    fromAccount.withdraw(amount)
    toAccount.deposit(amount)