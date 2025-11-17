import unittest
from datetime import date
from app.models.User_class import User, role_enum, status_enum

class TestUser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 可选：这里不做重活，仅占位
        pass

    def test_default_values(self):
        u = User()
        self.assertEqual(u.status, status_enum.active)
        self.assertEqual(u.role, role_enum.user)
        self.assertIsInstance(u.datetime, date)
        self.assertEqual(u.userId, "")
        self.assertEqual(u.username, "")

    def test_constructor_sets_fields(self):
        u = User()
        u.constructor("Lizhenyu123", "Zhenyu", "0123", role_enum.admin, status_enum.banned)
        self.assertEqual(u.userId, "Lizhenyu123")
        self.assertEqual(u.username, "Zhenyu")
        self.assertEqual(u.passwordHash, "0123")
        self.assertEqual(u.role, role_enum.admin)
        self.assertEqual(u.status, status_enum.banned)

    # def test_add_function(self):
    #     u = User()
    #     self.assertEqual(u.add(2, 3), 5)
    #     self.assertEqual(u.add(-1, 1), 0)

if __name__ == "__main__":
    unittest.main()