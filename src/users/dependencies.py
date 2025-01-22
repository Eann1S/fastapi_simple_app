from fastapi import HTTPException
from sqlmodel import select
from .schemas import UserCreate
from ..database import SessionDep
from .models import User


def is_user_id_valid(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return user


async def is_user_email_valid(userCreate: UserCreate, session: SessionDep):
    print(userCreate)
    user = session.exec(select(User).where(User.email == userCreate.email)).first()
    if user:
        raise HTTPException(status_code=400, detail=f"User with email {userCreate.email} already exists")
    return userCreate
