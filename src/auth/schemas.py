from pydantic import EmailStr
from sqlmodel import SQLModel


class RegisterSchema(SQLModel):
    email: EmailStr
    password: str


class Token(SQLModel):
    access_token: str
    token_type: str
