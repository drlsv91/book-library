from fastapi import APIRouter, Depends, HTTPException, status
from app.models import (
    BookPublic,
    Book,
    BooksPublic,
    BorrowedBookCreate,
    BorrowedBook,
)
from typing import Annotated
from app.api.deps import SessionDep, CurrentUser
from typing import Any
import uuid
from sqlmodel import select, func
from typing import List
from datetime import datetime, timedelta
from app.events import publish_event

router = APIRouter(prefix="/books", tags=["Bool"])


@router.get("/", response_model=BooksPublic)
def read_books(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    category: str | None = None,
    publisher: str | None = None,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve Books.
    """
    count_statement = select(func.count()).select_from(Book)
    count = session.exec(count_statement).one()
    query = select(Book)
    if category is not None:
        query = query.where(Book.category == category)

    if publisher is not None:
        query = query.where(Book.author == publisher)

    statement = query.offset(skip).limit(limit)
    books = session.exec(statement).all()
    return BooksPublic(data=books, count=count)


@router.get("/availiable", response_model=BooksPublic)
def read_available_books(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve Books.
    """

    count_statement = select(func.count()).select_from(Book)
    count = session.exec(count_statement).one()

    query = select(Book).where(Book.is_available == True)
    statement = query.offset(skip).limit(limit)
    books = session.exec(statement).all()

    return BooksPublic(data=books, count=count)


@router.post("/borrow", response_model=BooksPublic)
def borrow_book(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    borrow_data: Annotated[List[BorrowedBookCreate], Depends()],
) -> Any:
    """
    Borrow Books.
    """
    create_data = []
    for data in borrow_data:
        return_date = datetime.now() + timedelta(days=data.period_in_days)
        statement = select(Book).where(Book.id == data.book_id)
        book = session.exec(statement).first()
        if book is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book({data.id}) not found",
            )
        db_borrowed_book = BorrowedBook.model_validate(
            data,
            update={
                "user_id": current_user.id,
                "return_date": return_date,
                "book_id": book.id,
            },
        )
        create_data.append(db_borrowed_book)

    session.add_all(create_data)
    session.commit()
    session.refresh(create_data)
    publish_event(
        "frontend_events",
        {
            "event": "new_borrowed_book",
            "data": [item.model_dump(mode="json") for item in create_data],
        },
    )
    return create_data


@router.get("/{book_id}", response_model=BookPublic)
def delete_book(
    *, session: SessionDep, current_user: CurrentUser, book_id: uuid.UUID
) -> Any:
    """
    Get a Book by ID
    """
    statement = select(Book).where(Book.id == book_id)
    db_book = session.exec(statement).first()
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    return db_book
