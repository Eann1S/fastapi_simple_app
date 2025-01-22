from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine
from src.config import settings

engine = create_engine(settings.postgres_url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


SessionDep = Annotated[Session, Depends(get_session)]
