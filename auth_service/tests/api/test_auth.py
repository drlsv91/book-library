from fastapi.testclient import TestClient
from app.models import User
from app.core.config import settings
from app.core.security import ALGORITHM
import jwt


def test_login_access_token(client: TestClient, current_user: User, redis):

    response = client.post(
        f"{settings.API_V1_STR}/auth/login/access-token",
        data={
            "username": current_user.email,
            "password": "password",
            "grant_type": "password",
        },
    )

    assert response.status_code == 200

    data = response.json()

    access_token = data["access_token"]
    try:
        decoded_token = jwt.decode(
            access_token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM],
        )
    except Exception as e:
        assert False, f"Failed to decode JWT: {e}"

    assert "sub" in decoded_token, "JWT should contain a 'sub' claim"
    assert "payload" in decoded_token, "JWT should contain a 'payload' claim"
    assert "exp" in decoded_token, "JWT should contain a 'exp' claim"
    assert decoded_token["sub"] == str(current_user.id)
