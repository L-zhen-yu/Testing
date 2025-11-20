import os
import json
import pytest
from app.models.userMethods import user_signup, FILE_PATH
from app.models.user import User

def test_login():
    result = user_signup("testuser", "password123")
    assert result == 1

def test_login_password_no_num():
    result = user_signup("testuser2", "password")
    assert result == -2

def test_login_password_no_char():
    result = user_signup("testuser3", "123456789")
    assert result == -2

def test_login_password_too_short():
    result = user_signup("testuser4", "a1")
    assert result == -1

def test_login_sameUser():
    result = user_signup("testuser", "password321")
    assert result == -3

def test_user_class():
    user = User()
    signup_result = user.signup("classuser", "classpass123")
    assert signup_result == "User created"
    assert user.get_logged_in_status() == True
    assert user.get_username() == "classuser"

    logout_result = user.logout()
    assert logout_result == "Logged out successfully"
    assert user.get_logged_in_status() == False
    assert user.get_username() == "guest"

    login_result = user.login("classuser", "classpass123")
    assert login_result == "Login successful"
    assert user.get_logged_in_status() == True
    assert user.get_username() == "classuser"
    assert user.get_banned_status() == False

def test_admin_status():
    admin_user = User()
    admin_user.signup("adminuser", "adminpass123")
    admin_user.set_admin(True)
    assert admin_user.is_admin == True

    admin_user.set_admin(False)
    assert admin_user.is_admin == False

def test_ban_status():
    ban_user = User()
    ban_user.signup("banuser", "banpass123")
    ban_user.set_banned_status(True)
    assert ban_user.is_banned == True

    ban_user.set_banned_status(False)
    assert ban_user.is_banned == False