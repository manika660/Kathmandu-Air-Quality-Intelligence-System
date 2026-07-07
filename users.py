users = {
    "admin": "1234",
    "user": "air123"
}


def login(username, password):

    if username in users:
        if users[username] == password:
            return True

    return False