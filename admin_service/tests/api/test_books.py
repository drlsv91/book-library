from fastapi.testclient import TestClient
from sqlmodel import Session
from app.models import User, Book
from app.core.config import settings
from datetime import datetime
from sqlmodel import select
import json


def test_create_book(
    client: TestClient, current_user: User, user_token_headers: dict[str, str], redis
):

    response = client.post(
        f"{settings.API_V1_STR}/books/",
        headers=user_token_headers,
        json={
            "title": "the date of night",
            "author": "Apress",
            "category": "technology",
            "published_date": "2025-03-04T20:16:43.609Z",
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["id"] is not None
    assert data["title"] == "the date of night"
    assert data["author"] == "Apress"
    assert data["category"] == "technology"
    assert data["published_date"] is not None
    assert data["is_available"] == True
    assert data["add_by_id"] == str(current_user.id)


def test_read_books(
    client: TestClient,
    session: Session,
    current_user: User,
    user_token_headers: dict[str, str],
):

    book1 = Book(
        title="the date of night",
        author="Apress",
        category="technology",
        published_date=datetime.now(),
        is_available=True,
        add_by_id=current_user.id,
    )
    book2 = Book(
        title="Best of Alariya",
        author="Simon",
        category="Friction",
        published_date=datetime.now(),
        is_available=True,
        add_by_id=current_user.id,
    )
    session.add_all([book1, book2])
    session.commit()

    response = client.get(
        f"{settings.API_V1_STR}/books/",
        headers=user_token_headers,
    )

    assert response.status_code == 200
    data = response.json()

    books_in_response = data["data"]

    assert len(data["data"]) >= 2

    assert any(book["title"] == "the date of night" for book in books_in_response)
    assert any(book["title"] == "Best of Alariya" for book in books_in_response)

    assert any(book["category"] == "technology" for book in books_in_response)
    assert any(book["category"] == "Friction" for book in books_in_response)
    assert any(book["add_by_id"] == str(current_user.id) for book in books_in_response)


def test_delete_book(
    client: TestClient,
    session: Session,
    current_user: User,
    user_token_headers: dict[str, str],
    redis,
):

    book = Book(
        title="delete me",
        author="Apress",
        category="technology",
        published_date=datetime.now(),
        is_available=True,
        add_by_id=current_user.id,
    )

    session.add(book)
    session.commit()

    response = client.delete(
        f"{settings.API_V1_STR}/books/{book.id}",
        headers=user_token_headers,
    )

    assert response.status_code == 200
    data = response.json()

    statement = select(Book).where(Book.id == book.id)
    db_book = session.exec(statement).first()
    assert db_book is None
    assert data["title"] == "delete me"
