import unittest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.models.user import User
from app.models import userMethods

# Minimal FastAPI app exposing endpoints that wrap the User behavior

app = FastAPI()
user_instance = User()


@app.get("/user/state")
def get_user_state():
    """
    Return the current in-memory User state.
    """
    return {
        "logged_in": user_instance.logged_in,
        "username": user_instance.username,
        "is_admin": user_instance.is_admin,
        "is_banned": user_instance.is_banned,
    }


@app.post("/user/signup")
def signup(username: str, password: str):
    """
    Wrap User.signup(...) so tests can exercise it via HTTP.
    """
    message = user_instance.signup(username, password)
    return {
        "message": message,
        "logged_in": user_instance.logged_in,
        "username": user_instance.username,
        "is_admin": user_instance.is_admin,
        "is_banned": user_instance.is_banned,
    }


@app.post("/user/login")
def login(username: str, password: str):
    """
    Wrap User.login(...) so tests can exercise all login branches.
    """
    message = user_instance.login(username, password)
    return {
        "message": message,
        "logged_in": user_instance.logged_in,
        "username": user_instance.username,
        "is_admin": user_instance.is_admin,
        "is_banned": user_instance.is_banned,
    }


client = TestClient(app)


class TestUserAPI(unittest.TestCase):
    """
    Tests for the User / userMethods behavior via FastAPI endpoints.
    This file is designed to match the equivalence classes in your
    pre-lab document (signup + login return codes).
    """

    @classmethod
    def setUpClass(cls):
        # Backup original users.json so we can restore it later.
        cls._original_users = userMethods.load_users()

    @classmethod
    def tearDownClass(cls):
        # Restore original users.json after all tests have finished.
        userMethods.save_users(cls._original_users)

    def setUp(self):
        # Start each test with a clean user store and a fresh in-memory User.
        userMethods.save_users({})
        user_instance.logout()

    # ------------------------ basic state ------------------------

    def test_default_values(self):
        """
        After __init__, the default User state should be:
        - not logged in
        - username 'guest'
        - not admin
        - not banned
        """
        resp = client.get("/user/state")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        self.assertFalse(data["logged_in"])
        self.assertEqual(data["username"], "guest")
        self.assertFalse(data["is_admin"])
        self.assertFalse(data["is_banned"])

    # ------------------------ signup tests ------------------------

    def test_signup_success(self):
        """
        Successful signup: valid password and new username.
        Should:
        - return message 'User created'
        - log the user in
        - set username correctly
        - store the user in users.json
        """
        resp = client.post(
            "/user/signup", params={"username": "alice", "password": "Abc12345"}
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        self.assertEqual(data["message"], "User created")
        self.assertTrue(data["logged_in"])
        self.assertEqual(data["username"], "alice")
        self.assertFalse(data["is_admin"])
        self.assertFalse(data["is_banned"])

        users = userMethods.load_users()
        self.assertIn("alice", users)

    def test_signup_password_too_short(self):
        """
        Password length < 8 → 'Password too short'.
        No user should be created and User should remain guest.
        """
        resp = client.post(
            "/user/signup", params={"username": "shortuser", "password": "A1b2c3"}
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        self.assertEqual(data["message"], "Password too short")
        self.assertFalse(data["logged_in"])
        self.assertEqual(data["username"], "guest")

        users = userMethods.load_users()
        self.assertNotIn("shortuser", users)

    def test_signup_password_must_contain_letters_and_numbers(self):
        """
        Password only letters OR only digits should both trigger:
        'Password must contain both letters and numbers'.
        """
        # Only letters
        resp_letters = client.post(
            "/user/signup", params={"username": "user_letters", "password": "abcdefgh"}
        )
        self.assertEqual(resp_letters.status_code, 200)
        data_letters = resp_letters.json()
        self.assertEqual(
            data_letters["message"], "Password must contain both letters and numbers"
        )

        # Only digits
        user_instance.logout()
        userMethods.save_users({})
        resp_digits = client.post(
            "/user/signup", params={"username": "user_digits", "password": "12345678"}
        )
        self.assertEqual(resp_digits.status_code, 200)
        data_digits = resp_digits.json()
        self.assertEqual(
            data_digits["message"], "Password must contain both letters and numbers"
        )

        users = userMethods.load_users()
        self.assertNotIn("user_letters", users)
        self.assertNotIn("user_digits", users)

    def test_signup_username_already_taken(self):
        """
        If the username is already present in users.json, signup should
        return 'Username already taken' and not overwrite the existing user.
        """
        # First successful signup
        client.post(
            "/user/signup", params={"username": "alice", "password": "Abc12345"}
        )
        users_before = userMethods.load_users()

        # Second attempt with same username
        user_instance.logout()
        resp = client.post(
            "/user/signup", params={"username": "alice", "password": "Different1"}
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        self.assertEqual(data["message"], "Username already taken")

        users_after = userMethods.load_users()
        self.assertEqual(users_before, users_after)

    # ------------------------ login tests ------------------------

    def test_login_success_normal_user(self):
        """
        Normal login flow:
        - user exists
        - correct password
        Should return 'Login successful' and set logged_in True.
        """
        userMethods.user_signup("alice", "Abc12345")
        resp = client.post(
            "/user/login", params={"username": "alice", "password": "Abc12345"}
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        self.assertEqual(data["message"], "Login successful")
        self.assertTrue(data["logged_in"])
        self.assertEqual(data["username"], "alice")
        self.assertFalse(data["is_admin"])
        self.assertFalse(data["is_banned"])

    def test_login_admin_user(self):
        """
        Admin login flow:
        - user created with is_admin=True
        Should return 'Admin login successful' and set is_admin True.
        """
        userMethods.user_signup("admin", "Admin1234", is_admin=True)
        resp = client.post(
            "/user/login", params={"username": "admin", "password": "Admin1234"}
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        self.assertEqual(data["message"], "Admin login successful")
        self.assertTrue(data["logged_in"])
        self.assertEqual(data["username"], "admin")
        self.assertTrue(data["is_admin"])
        self.assertFalse(data["is_banned"])

    def test_login_wrong_username_or_password(self):
        """
        Wrong username or password should return:
        'Password or Username incorrect' and keep user logged out.
        """
        userMethods.user_signup("alice", "Abc12345")

        resp = client.post(
            "/user/login", params={"username": "alice", "password": "Wrong123"}
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        self.assertEqual(data["message"], "Password or Username incorrect")
        # State should remain default guest
        self.assertFalse(data["logged_in"])
        self.assertEqual(data["username"], "guest")

    def test_login_banned_user(self):
        """
        If the user is marked as banned in users.json, login should:
        - return 'User is banned'
        - set logged_in True and is_banned True on the User object.
        """
        userMethods.user_signup("alice", "Abc12345")
        userMethods.set_ban_status("alice", True)

        resp = client.post(
            "/user/login", params={"username": "alice", "password": "Abc12345"}
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        self.assertEqual(data["message"], "User is banned")
        self.assertTrue(data["logged_in"])
        self.assertEqual(data["username"], "alice")
        self.assertTrue(data["is_banned"])


if __name__ == "__main__":
    unittest.main()
