import logging
import time
from functools import wraps

from aop_example.database import IN_MEMORY_DB

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def logged(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        logging.debug(f"Called {func.__name__} {args} {kwargs}")
        func(*args, **kwargs)

    return wrapped


def throttled(max_frequency_in_millis):
    time_of_last_call = time.time() - max_frequency_in_millis
    def inner(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            nonlocal time_of_last_call
            current_time = time.time()
            millis_since_last_call = (current_time - time_of_last_call) * 1000
            if millis_since_last_call < max_frequency_in_millis:
                raise Exception(f"Calls to {func.__name__} are limited to every {max_frequency_in_millis}ms")
            time_of_last_call = current_time
            func(*args, **kwargs)

        return wrapped

    return inner

def access_controlled(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            user_token = kwargs['user_token']
        except KeyError:
            raise Exception(f"No user_token keyword was provided to function '{func.__name__}'")
        if user_token.is_valid():
            kwargs.pop("user_token")
            func(*args, **kwargs)
        else:
            raise Exception(f"Received invalid token for user '{user_token.username}'")

    return wrapped

def database_backed(Clazz):

    IN_MEMORY_DB.create_table(Clazz.__name__)

    def setter(obj, key, value):
        IN_MEMORY_DB.set_value(Clazz.__name__, hash(obj), key, value)

    def getter(obj, key):
        return IN_MEMORY_DB.get_value(Clazz.__name__, hash(obj), key)

    Clazz.__setattr__ = setter
    Clazz.__getattr__ = getter

    return Clazz

def atomic(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        IN_MEMORY_DB.begin_transaction()
        try:
            func(*args, **kwargs)
            IN_MEMORY_DB.commit()
        except:
            IN_MEMORY_DB.rollback()
            raise


    return wrapped