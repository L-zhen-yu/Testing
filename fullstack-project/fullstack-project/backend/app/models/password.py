import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

hashed = hash_password("mypassword123")
print(hashed)

