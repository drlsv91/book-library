from datetime import datetime, timezone, timedelta
import jwt
from app.core.security import ALGORITHM
from app.core.config import settings
from app.models import User


def user_authentication_headers(*, user: User) -> dict[str, str]:
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {
        "exp": expire,
        "sub": str(user.id),
        "payload": user.model_dump(mode="json"),
    }

    auth_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers
