from fastapi import APIRouter, HTTPException, status
from app.models import UserPublic, UserEnroll, User
from typing import Any
from app.api.deps import SessionDep
from sqlmodel import select
from app.events import publish_event


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/enroll", response_model=UserPublic)
def register_user(session: SessionDep, user_in: UserEnroll) -> Any:
    """
    Create new user without the need to be logged in.
    """
    statement = select(User).where(User.email == user_in.email)
    user_exist = session.exec(statement).first()
    print(user_exist)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user with this email already enrolled.",
        )

    user_create = User.model_validate(user_in)
    session.add(user_create)
    session.commit()
    session.refresh(user_create)
    user_payload = user_create.model_dump(mode="json")
    user_payload.update({"password": user_in.password})
    publish_event(
        "frontend_events",
        {"event": "user_enrolled", "user": user_payload},
    )
    return user_create
