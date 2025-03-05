import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, delete, StaticPool, SQLModel
from fakeredis import FakeRedis
from app.main import app
from app.models import User
from app.api.deps import get_db, get_current_user
from tests.utils.user import user_authentication_headers
from unittest.mock import patch


db = "sqlite://"


@pytest.fixture(name="session", scope="module")
def session():
    engine = create_engine(
        db, connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client(session: Session, redis):

    def override_get_db():
        return session

    with patch("app.events.redis_client", redis):
        app.dependency_overrides[get_db] = override_get_db
        client = TestClient(app)
        yield client
        app.dependency_overrides.clear()


@pytest.fixture(name="current_user", scope="module")
def sample_user(session: Session):
    user = User(first_name="Jane", last_name="Doe", email="jane.doe@example.com")
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def redis():
    return FakeRedis()


@pytest.fixture(scope="module")
def user_token_headers(current_user: User):
    return user_authentication_headers(user=current_user)


@pytest.fixture(scope="module")
def override_get_current_user(current_user: User):
    def _override_get_current_user():
        return current_user

    app.dependency_overrides[get_current_user] = _override_get_current_user
