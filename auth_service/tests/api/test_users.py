from fastapi.testclient import TestClient
from app.core.config import settings
from tests.utils.utils import random_email, random_lower_string
from app.models import User


def test_register_user(client: TestClient, redis):
    email = random_email()
    password = random_lower_string()

    response = client.post(
        f"{settings.API_V1_STR}/users/signup",
        json={
            "email": email,
            "password": password,
            "first_name": random_lower_string(),
            "last_name": random_lower_string(),
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == email
    assert data["id"] is not None
    assert data["is_active"] is True
    assert data["first_name"] is not None
    assert data["last_name"] is not None
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


def test_read_me(
    client: TestClient, current_user: User, user_token_headers: dict[str, str]
):
    response = client.get(f"{settings.API_V1_STR}/users/me", headers=user_token_headers)
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == str(current_user.id)
    assert data["email"] == str(current_user.email)
    assert data["is_active"] == current_user.is_active
