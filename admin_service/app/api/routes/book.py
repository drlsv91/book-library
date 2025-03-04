from fastapi import APIRouter, Depends, HTTPException, status
from app.models import BookPublic, BookCreate, Book, BooksPublic

from app.api.deps import SessionDep, CurrentUser, get_current_user
from typing import Any
import uuid
from sqlmodel import select, func, desc
from app.events import publish_event

router = APIRouter(prefix="/books", tags=["Book"])


@router.post("/", response_model=BookPublic)
def add_book(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    book_data: BookCreate,
) -> Any:
    """
    Add new Book.
    """
    db_book = Book.model_validate(book_data, update={"add_by_id": current_user.id})
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    publish_event(
        "admin_events", {"event": "new_book", "data": db_book.model_dump(mode="json")}
    )
    return db_book


@router.get("/", dependencies=[Depends(get_current_user)], response_model=BooksPublic)
def read_books(
    *,
    session: SessionDep,
    is_available: bool | None = None,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve Books.
    """
    query = select(Book)
    count_statement = select(func.count()).select_from(Book)
    count = session.exec(count_statement).one()

    if is_available is not None:
        query = query.where(Book.is_available == is_available)

    statement = query.order_by(desc(Book.created_at)).offset(skip).limit(limit)
    books = session.exec(statement).all()

    return BooksPublic(data=books, count=count)


@router.delete(
    "/{book_id}", dependencies=[Depends(get_current_user)], response_model=BookPublic
)
def delete_book(*, session: SessionDep, book_id: uuid.UUID) -> Any:
    """
    Delete a Book by ID
    """
    statement = select(Book).where(Book.id == book_id)
    db_book = session.exec(statement).first()
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    session.delete(db_book)
    session.commit()
    publish_event(
        "admin_events",
        {"event": "delete_book", "data": db_book.model_dump(mode="json")},
    )
    return db_book
