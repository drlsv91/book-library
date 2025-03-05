from fastapi.testclient import TestClient
from sqlmodel import Session
from app.models import User, BorrowedBook
from app.core.config import settings
import uuid
from datetime import datetime
from sqlmodel import select


def test_read_users(
    client: TestClient, session: Session, user_token_headers: dict[str, str]
):

    user1 = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    user2 = User(first_name="Mary", last_name="jack", email="jack.doe@example.com")
    session.add_all([user1, user2])
    session.commit()

    response = client.get(
        f"{settings.API_V1_STR}/users/",
        headers=user_token_headers,
    )

    assert response.status_code == 200
    data = response.json()

    users_in_response = data["data"]

    assert len(data["data"]) == 3
    assert data.get("count") == 3
    assert any(user["email"] == "john.doe@example.com" for user in users_in_response)
    assert any(user["email"] == "jack.doe@example.com" for user in users_in_response)

    for user in users_in_response:
        assert user["id"] is not None, f"User {user['email']} has no ID in the response"

    statement = select(User)
    users_in_db = session.exec(statement).all()
    assert len(users_in_db) == 3
    assert any(user.email == "john.doe@example.com" for user in users_in_db)
    assert any(user.email == "jack.doe@example.com" for user in users_in_db)
    for user in users_in_db:
        assert user.id is not None, f"User {user.email} has no ID in the database"


def test_read_users_books(
    client: TestClient,
    session: Session,
    current_user: User,
    user_token_headers: dict[str, str],
):

    book_id = uuid.uuid4()
    book = BorrowedBook(
        user_id=current_user.id,
        book_id=book_id,
        borrow_date=datetime.now(),
        return_date=datetime.now(),
        period_in_days=7,
    )
    session.add(book)
    session.commit()

    response = client.get(
        f"{settings.API_V1_STR}/users/books", headers=user_token_headers
    )

    assert response.status_code == 200
    payload = response.json()
    result = payload["data"]

    assert len(result) == 1

    assert str(result[0]["user_id"]) == str(current_user.id)
    assert result[0]["book_id"] == str(book_id)
    assert result[0]["period_in_days"] == 7
    assert result[0]["borrow_date"] is not None
    assert result[0]["return_date"] is not None
