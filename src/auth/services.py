from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from ..users.services import create_user, get_user_by_email, user_exists_by_email

from .utils import create_access_token, hash_password, verify_password

from .exceptions import user_already_exists, invalid_credentials
from .schemas import RegisterSchema, Token


def register_user(register_schema: RegisterSchema, session: Session):
    hashed_password = hash_password(register_schema.password)
    exists = user_exists_by_email(register_schema.email, session)
    if exists:
        raise user_already_exists
    user = create_user(register_schema, session, update={"hashed_password": hashed_password})
    return user


def authenticate_user(form_data: OAuth2PasswordRequestForm, session: Session):
    user = get_user_by_email(form_data.username, session)
    if not verify_password(form_data.password, user.hashed_password):
        raise invalid_credentials
    token = create_access_token({"sub": str(user.id)})
    return Token(access_token=token, token_type="bearer")
