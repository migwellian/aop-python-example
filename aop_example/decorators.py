import logging
import time

from aop_example.accounts import access_control

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def logged(func):
    def wrapped(*args, **kwargs):
        logging.debug(f"Called {func.__name__} {args} {kwargs}")
        func(*args, **kwargs)

    return wrapped


def throttled(max_frequency_in_millis):
    time_of_last_call = time.time() - max_frequency_in_millis
    def inner(func):
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
    def wrapped(*args, **kwargs):
        if access_control.current_user is None:
            raise Exception(f"You must log in to perform {func.__name__}")
        else:
            func(*args, **kwargs)

    return wrapped
