from fastapi.testclient import TestClient
from sqlmodel import Session
from app.models import User, Book
from app.core.config import settings
from datetime import datetime
from sqlmodel import select
import json


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


def test_read_available_books(
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
        is_available=False,
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
        f"{settings.API_V1_STR}/books/availiable",
        headers=user_token_headers,
    )

    assert response.status_code == 200
    data = response.json()

    books_in_response = data["data"]

    for book in books_in_response:
        assert book["is_available"] is True, f"Book {book['title']} is not available"


def test_read_book(
    client: TestClient,
    session: Session,
    current_user: User,
    user_token_headers: dict[str, str],
):

    book = Book(
        title="the date of night",
        author="Apress",
        category="technology",
        published_date=datetime.now(),
        is_available=True,
        add_by_id=current_user.id,
    )

    session.add(book)
    session.commit()

    response = client.get(
        f"{settings.API_V1_STR}/books/{book.id}/",
        headers=user_token_headers,
    )

    assert response.status_code == 200
    data = response.json()

    assert data["title"] == book.title
    assert data["id"] == str(book.id)


def test_borrow_books(
    client: TestClient,
    session: Session,
    current_user: User,
    user_token_headers: dict[str, str],
):

    book = Book(
        title="the date of night",
        author="Apress",
        category="technology",
        published_date=datetime.now(),
        is_available=True,
        add_by_id=current_user.id,
    )

    session.add(book)
    session.commit()

    response = client.post(
        f"{settings.API_V1_STR}/books/borrow",
        headers=user_token_headers,
        json=[{"book_id": str(book.id), "period_in_days": 7}],
    )

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["book_id"] == str(book.id)


def test_borrow_unavailable_books(
    client: TestClient,
    session: Session,
    current_user: User,
    user_token_headers: dict[str, str],
):

    book = Book(
        title="the date of night",
        author="Apress",
        category="technology",
        published_date=datetime.now(),
        is_available=False,
        add_by_id=current_user.id,
    )

    session.add(book)
    session.commit()

    response = client.post(
        f"{settings.API_V1_STR}/books/borrow",
        headers=user_token_headers,
        json=[{"book_id": str(book.id), "period_in_days": 7}],
    )

    assert response.status_code == 400
    data = response.json()

    assert data == {"detail": "Book(the date of night) is not available"}
