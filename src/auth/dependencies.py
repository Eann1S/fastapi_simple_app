from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from ..users.services import get_user_by_id

from .utils import verify_access_token

from ..database import SessionDep


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep):
    user_id = verify_access_token(token)
    user = get_user_by_id(user_id, session)
    print(f"\ntoken = {token}, \nuser = {user}\n")
    return user
