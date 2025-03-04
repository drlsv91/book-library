from fastapi import APIRouter, Depends
from app.models import (
    UsersPublic,
    User,
    BorrowedBook,
    BorrowedBooksPublic,
)
from app.api.deps import SessionDep, get_current_user
from typing import Any
from sqlmodel import select, func

router = APIRouter(prefix="/users", tags=["User"])


@router.get("/", dependencies=[Depends(get_current_user)], response_model=UsersPublic)
def read_users(*, session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve Users.
    """
    count_statement = select(func.count()).select_from(User)
    count = session.exec(count_statement).one()

    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()

    return UsersPublic(data=users, count=count)


@router.get(
    "/books",
    dependencies=[Depends(get_current_user)],
    response_model=BorrowedBooksPublic,
)
def read_books(*, session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve Borrowed books.
    """
    count_statement = select(func.count()).select_from(BorrowedBook)
    count = session.exec(count_statement).one()

    statement = select(BorrowedBook).offset(skip).limit(limit)
    books = session.exec(statement).all()

    return BorrowedBooksPublic(data=books, count=count)
