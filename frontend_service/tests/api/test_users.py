from fastapi.testclient import TestClient
from app.core.config import settings
from tests.utils.utils import random_email, random_lower_string


def test_register_user(client: TestClient):

    email = random_email()
    password = random_lower_string()

    response = client.post(
        f"{settings.API_V1_STR}/users/enroll",
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
