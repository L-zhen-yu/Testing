import json 
import os
from app.models.password import hash_password

FILE_PATH = os.path.join(os.path.dirname(__file__), "users.json")


def load_users():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

def save_users(users):
    with open(FILE_PATH, "w") as file:
        json.dump(users, file, indent=4)


def user_signup (username: str, password: str, is_admin: bool = False):
    users = load_users()

    if len(password) < 8:
        return -1   # Code for password too short
    
    if password.isalpha() or password.isdigit():
        return -2  # Code for password must contain both letters and numbers
    
    if username in users:
        return -3 # Code for username already taken
    
    hashword = hash_password(password)
    users[username] = {
        "password": hashword,
        "is_admin": is_admin,
        "is_banned": False
    }
    save_users(users)
    return 1 # Code for successful user creation

def user_login(username: str, password: str):
    users = load_users()
    hashword = hash_password(password)

    if username not in users: 
        return -1 # Code for incorrect username or password
    if users[username]["password"] != hashword:
        return -1 # Code for incorrect username or password
    if users[username]["is_banned"] == True:
        return -2 # Code for banned user
    if users[username]["is_admin"] == True:
        return 2 # Code for admin login
    else: 
        return 1 # Code for successful login
    
def set_admin_status(username: str, is_admin: bool):
    users = load_users()
    if username in users:
        users[username]["is_admin"] = is_admin
        save_users(users)
        return True
    return False

def set_ban_status(username: str, is_banned: bool):
    users = load_users()
    if username in users:
        users[username]["is_banned"] = is_banned
        save_users(users)
        return True
    return False