from enum import Enum
from datetime import date

class role_enum(Enum):
    user = "user"
    admin = "admin"

class status_enum(Enum):
    active = "active"
    banned = "banned"

class User:
    def __init__(self):
        self.userId = ""
        self.username = ""
        self.passwordHash = ""
        self.role = role_enum.user
        self.datetime = date.today()
        self.status = status_enum.active

    def constructor(self, userId, username, passwordHash, role, status):
        # TODO 完成初始化（你已完成）
        self.userId = userId
        self.username = username
        self.passwordHash = passwordHash
        self.role = role
        self.status = status

    def add(self, a, b):
        return a + b