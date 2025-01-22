from contextlib import asynccontextmanager
from fastapi import FastAPI
from .users.routes import router as users
from .database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("starting")
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=users)
