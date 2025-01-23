from fastapi.testclient import TestClient
from src.main import app
from src.database import get_session
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from src.users.models import User
import pytest


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app=app)
    yield client
    app.dependency_overrides.clear()


def test_create_user(client: TestClient):
    response = client.post("/users", json={"email": "test@wp.pl", "password": "test123"})
    data = response.json()
    
    assert response.status_code == 200
    assert data["email"] == "test@wp.pl"
    assert data["id"] is not None


def test_get_user(session: Session, client: TestClient):
    user = User(email="test@wp.pl", hashed_password="test123")
    session.add(user)
    session.commit()
    session.refresh(user)

    response = client.get(f"/users/{user.id}")
    data = response.json()
    
    assert response.status_code == 200
    assert data["email"] == "test@wp.pl"
    assert data["id"] == user.id
