# yes this is a terrible access control mechanism!
# for demo purposes only

current_user = None

passwords = {"admin": "admin"}

def login(username, password):
    if is_valid(username, password):
        global current_user
        current_user = username

def logout():
    global current_user
    current_user = None

def is_valid(username, password):
    return passwords[username] == password

