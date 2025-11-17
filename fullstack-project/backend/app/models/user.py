class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.logged_in = False

    def registerUser(self, existing_users):
        if self.username in existing_users:
            return "Username already exists"
        existing_users.append(self.username)
        return "User registered successfully"

    def loginUser(self, stored_password):
        if self.password == stored_password:
            self.logged_in = True
            return True
        return False
