import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def logged(func):
    def wrapped(*args, **kwargs):
        logging.debug(f"Called {func.__name__} {args} {kwargs}")
        func(*args, **kwargs)

    return wrapped