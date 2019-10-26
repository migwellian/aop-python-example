
def logged(func):
    def wrapped(*args, **kwargs):
        print(f"Called {func.__name__} {args} {kwargs}")
        func(*args, **kwargs)

    return wrapped