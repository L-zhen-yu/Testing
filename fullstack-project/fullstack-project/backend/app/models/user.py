from app.models.userMethods import user_signup, user_login, set_admin_status, set_ban_status


class User():
    def __init__(self):
        self.logged_in = False
        self.username = 'guest'
        self.is_admin = False
        self.is_banned = False

    def login(self, NewUsername, password):
        result = user_login(NewUsername, password)
        if result == 1:
            self.logged_in = True
            self.username = NewUsername
            return "Login successful"
        if result == 2:
            self.logged_in = True
            self.username = NewUsername
            self.is_admin = True
            return "Admin login successful"
        if result == -1:
            return "Password or Username incorrect"
        if result == -2:
            self.logged_in = True
            self.username = NewUsername
            self.is_banned = True
            return "User is banned"
        
    def logout(self):
        self.logged_in = False
        self.username = 'guest'
        self.is_admin = False
        self.is_banned = False
        return "Logged out successfully"
    
    def signup(self, NewUsername, password):
        result = user_signup(NewUsername, password)
        if result == 1:
            self.logged_in = True
            self.username = NewUsername
            return "User created"
        if result == -1:
            return "Password too short"
        if result == -2:
            return "Password must contain both letters and numbers"
        if result == -3:
            return "Username already taken"
        
    def set_admin(self, status: bool):
        if self.logged_in:
            set_admin_status(self.username, status)
            self.is_admin = status
            return True
        
    
    def get_logged_in_status(self):
        return self.logged_in
    
    def get_username(self):
        return self.username
    
    def get_admin_status(self):
        return self.is_admin
    
    def get_banned_status(self):
        return self.is_banned
    
    def set_banned_status(self, status: bool):
        if self.logged_in:
            set_ban_status(self.username, status)
            self.is_banned = status
            return True
