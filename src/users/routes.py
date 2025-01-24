from typing import Annotated
from fastapi import APIRouter, Depends

from ..auth.dependencies import get_current_user

from .schemas import UserPublic

from .models import User


router = APIRouter(prefix="/users")


@router.get("/me", response_model=UserPublic)
def get_current_user(*, user: Annotated[User, Depends(get_current_user)]):
    return user
