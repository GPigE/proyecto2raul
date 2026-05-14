import os
from datetime import datetime, timedelta, timezone
from jose import jwt

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
EXPIRATION_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "3"))


def create_access_token(data: dict) -> str:
    assert SECRET_KEY is not None, "SECRET_KEY must be set"
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    assert SECRET_KEY is not None, "SECRET_KEY must be set"
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])