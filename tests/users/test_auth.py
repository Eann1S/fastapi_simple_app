from fastapi.testclient import TestClient
from src.main import app
from src.database import get_session
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
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


def test_register(client: TestClient):
    response = client.post("/register", json={"email": "test1@wp.pl", "password": "test123"})
    data = response.json()

    assert response.status_code == 200
    assert data["email"] == "test1@wp.pl"
    assert data["id"] is not None


def test_login(client: TestClient):
    register_user(json={"email": "test2@wp.pl", "password": "test123"}, client=client)

    response = client.post(
        "/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": "test2@wp.pl", "password": "test123"},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["access_token"] is not None
    assert data["token_type"] == "bearer"


def register_user(json: dict[str, str], client: TestClient):
    response = client.post("/register", json=json)
    data = response.json()
    return data
