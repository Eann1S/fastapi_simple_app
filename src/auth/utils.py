from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
from .exceptions import invalid_access_token

from ..config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(plain_password: str):
    return pwd_context.hash(plain_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    exp = datetime.now(timezone.utc) + timedelta(milliseconds=settings.jwt_exp_millis)
    to_encode.update({"exp": exp})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def verify_access_token(token: str) -> str:
    try:
        decoded_jwt = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except Exception as e:
        print(e)
        raise invalid_access_token
    sub = decoded_jwt.get('sub')
    if not sub:
        raise invalid_access_token
    return sub
