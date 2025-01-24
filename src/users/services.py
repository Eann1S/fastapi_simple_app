from typing import Any
from pydantic import EmailStr
from sqlmodel import Session, select

from .schemas import UserCreate
from .exceptions import user_not_found

from .models import User


def get_user_by_id(user_id: int, session: Session):
    user = session.get(User, user_id)
    if not user:
        raise user_not_found
    return user


def get_user_by_email(email: EmailStr, session: Session):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise user_not_found
    return user


def user_exists_by_email(email: EmailStr, session: Session):
    try:
        get_user_by_email(email, session)
    except Exception as e:
        print(e)
        return False
    return True


def create_user(user_create: UserCreate, session: Session, update: dict[str, Any] | None = None):
    user = User.model_validate(user_create, update=update)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
