# yes this is a terrible access control mechanism!
# for demo purposes only
import time

passwords = {"admin": "admin"}

class Token:
    def __init__(self, username, expiry_time):
        self.__username = username
        self.__expiry_time = expiry_time

    @property
    def username(self):
        return self.__username

    def is_valid(self):
        return self.__expiry_time > time.time()


def login(username, password):
    if is_valid(username, password):
        return Token(username, time.time() + 60)
    else:
        return Token(username, 0)


def is_valid(username, password):
    return passwords[username] == password

