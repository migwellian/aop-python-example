import pytest
import time

from aop_example.accounts.account import Account
from aop_example.accounts.transactions import transfer

def setup_function(function):
    time.sleep(0.1)


def test_you_can_make_a_transfer():
    from_account = Account("A123", 100)
    to_account = Account("B456", 100)
    transfer(from_account, to_account, amount=10)

    assert from_account.balance == 90
    assert to_account.balance == 110


def test_you_cannot_call_transfer_more_than_once_per_100ms():
    from_account = Account("A123", 100)
    to_account = Account("B456", 100)
    transfer(from_account, to_account, amount=10)
    with pytest.raises(Exception) as excinfo:
        transfer(from_account, to_account, amount=10)
    assert excinfo.value.args[0] == "Calls to wrapped are limited to every 100ms"


def test_you_can_call_transfer_again_after_100ms():
    from_account = Account("A123", 100)
    to_account = Account("B456", 100)
    transfer(from_account, to_account, amount=10)
    time.sleep(0.1)
    transfer(from_account, to_account, amount=10)

    assert from_account.balance == 80
    assert to_account.balance == 120