import sys, os

cur_path = os.path.dirname(os.path.abspath(__file__))
head, tail = os.path.split(os.path.split(cur_path)[0])
sys.path.insert(0, os.path.join(head, 'src'))
from typing import Any
from typing import Generator


import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from api.base import api_router
from db.db import get_db
from models.base import Base


def start_app():
    app = FastAPI()
    app.include_router(api_router)
    return app


SQLALCHEMY_DATABASE_URL = "sqlite:///test_sql_app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)  # Create the tables.
    _app = start_app()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(app: FastAPI, db_session: SessionTesting) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


def test_create_user(client):
    data = {"name":"Debug", "surname":"Boy", "email":"debugboy@gmail.com", "password":"no_bugs" }
    response = client.post("/users/create", json=data)
    assert response.status_code == 201
    assert response.json()["email"] == "debugboy@gmail.com"


def test_get_users(client):
    data = {"name":"Debug", "surname":"Boy", "email":"debugboy@gmail.com", "password":"no_bugs" }
    client.post("/users/create", json=data)
    response = client.get("/users/all")
    assert response.status_code == 200
    assert len(response.json()) > 0