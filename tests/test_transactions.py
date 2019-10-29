import pytest
import time

from aop_example.accounts import access_control
from aop_example.accounts.account import Account
from aop_example.accounts.transactions import transfer

def setup_function(function):
    time.sleep(0.1)

@pytest.fixture
def user_token():
    return access_control.login("admin", "admin")


def test_you_can_make_a_transfer(user_token):
    from_account = Account("A123", 100)
    to_account = Account("B456", 100)
    transfer(from_account, to_account, amount=10, user_token=user_token)

    assert from_account.balance == 90
    assert to_account.balance == 110


def test_you_cannot_call_transfer_more_than_once_per_100ms(user_token):
    from_account = Account("A123", 100)
    to_account = Account("B456", 100)
    transfer(from_account, to_account, amount=10, user_token=user_token)
    with pytest.raises(Exception) as excinfo:
        transfer(from_account, to_account, amount=10, user_token=user_token)
    assert excinfo.value.args[0] == "Calls to transfer are limited to every 100ms"


def test_you_can_call_transfer_again_after_100ms(user_token):
    from_account = Account("A123", 100)
    to_account = Account("B456", 100)
    transfer(from_account, to_account, amount=10, user_token=user_token)
    time.sleep(0.1)
    transfer(from_account, to_account, amount=10, user_token=user_token)

    assert from_account.balance == 80
    assert to_account.balance == 120


def test_the_user_must_be_logged_in_to_make_a_transaction():
    user_token = access_control.login("admin", "wrong_password")

    from_account = Account("A123", 100)
    to_account = Account("B456", 100)
    with pytest.raises(Exception) as excinfo:
        transfer(from_account, to_account, amount=10, user_token=user_token)
    assert excinfo.value.args[0] == "Received invalid token for user 'admin'"


def test_you_must_pass_in_a_user_token_even_though_its_not_declared_in_the_signature():
    from_account = Account("A123", 100)
    to_account = Account("B456", 100)
    with pytest.raises(Exception) as excinfo:
        transfer(from_account, to_account, amount=10)
    assert excinfo.value.args[0] == "No user_token keyword was provided to function 'transfer'"


def test_the_transaction_is_rolled_back_if_any_part_fails(user_token):
    from_account = Account("A123", 100)
    to_account = Account("B456", 100)
    to_account.freeze()

    with pytest.raises(Exception) as excinfo:
        transfer(from_account, to_account, amount=10, user_token=user_token)
    assert excinfo.value.args[0] == "Account B456 is inactive: cannot deposit funds"

    assert from_account.balance == 100
    assert to_account.balance == 100


