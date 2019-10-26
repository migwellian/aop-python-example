from aop_example.accounts.account import Account
from aop_example.accounts.transactions import transfer


def test_you_can_make_a_transfer():
    from_account = Account("A123", 100)
    to_account = Account("B456", 100)
    transfer(from_account, to_account, amount=10)

    assert from_account.balance == 90
    assert to_account.balance == 110