from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.models import Token, UserPublic
from app import crud
from app.core import security
from app.core.config import settings
from app.api.deps import SessionDep

router = APIRouter(prefix="/auth", tags=["login"])


@router.post("/login/access-token")
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for api requests
    """
    user = crud.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    user_data = UserPublic(**user.model_dump(mode="json"))

    return Token(
        access_token=security.create_access_token(
            user.id,
            expires_delta=access_token_expires,
            payload=user_data.model_dump(mode="json"),
        )
    )
