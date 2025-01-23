from typing import Annotated
from fastapi import APIRouter, Depends

from .dependencies import is_user_email_valid, is_user_id_valid

from .schemas import UserCreate, UserPublic
from ..database import SessionDep
from .models import User


router = APIRouter()


@router.post("/users", response_model=UserPublic)
def create_user(*, userCreate: UserCreate = Depends(is_user_email_valid), session: SessionDep):
    update_data = {"hashed_password": userCreate.password}
    user = User.model_validate(userCreate, update=update_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/users/{user_id}", response_model=UserPublic)
def get_user(*, user_id: int, user: User = Depends(is_user_id_valid)):
    return user
