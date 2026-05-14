from argon2 import PasswordHasher

ph = PasswordHasher()

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(hashed: str, password: str) -> bool:
    try:
        return ph.verify(hashed, password)
    except Exception:
        return False