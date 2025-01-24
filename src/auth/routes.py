from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from .services import authenticate_user, register_user

from ..users.schemas import UserPublic

from .schemas import RegisterSchema, Token
from ..database import SessionDep


router = APIRouter()


@router.post("/token", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    return authenticate_user(form_data, session)


@router.post("/register", response_model=UserPublic)
def register(register_schema: RegisterSchema, session: SessionDep):
    return register_user(register_schema, session)
