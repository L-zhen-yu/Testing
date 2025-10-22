import unittest
from app.models.User_class import User,role_enum,status_enum
class TestMain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 整个类开始前运行一次
        a=User()
        pass
    def test_constructor(self):
        a=User()

        self.assertEqual(a.status,status_enum.active)
    def test_constructor2(self):
        a=User()
        a.constructor("Lizhenyu123","Zhenyu","0123",role_enum.admin,status_enum.banned)
        self.assertEqual(a.status,status_enum.banned)
    def test_constructor3(self):
        a=User()
        a.constructor("DaSHABI","Zhenyu","0123",role_enum.admin,status_enum.banned)
        self.assertEqual(a.userId,"DaSHABI")



