import uuid
from sqlmodel import (
    Field,
    Relationship,
    SQLModel,
)

from typing import List
from datetime import datetime, timezone
from pydantic import EmailStr


class BookBase(SQLModel):
    title: str = Field(index=True, max_length=255)
    author: str = Field(index=True, max_length=255)
    category: str = Field(index=True, max_length=255)
    published_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_available: bool = Field(default=False)
    author_id: uuid.UUID
    add_by_id: uuid.UUID
    available_date: datetime | None = Field(default=None, nullable=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Book(BookBase, table=True):
    __tablename__ = "books"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    borrowed_books: List["BorrowedBook"] = Relationship(back_populates="book")


class BookCreate(SQLModel):
    title: str
    author: str
    published_date: datetime
    author_id: uuid.UUID


class UserBase(SQLModel):
    first_name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    email: EmailStr = Field(unique=True, index=True)
    is_active: bool = True


class User(UserBase, table=True):
    __tablename__ = "users"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    borrowed_books: List["BorrowedBook"] = Relationship(back_populates="user")

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserPublic(UserBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class UserEnroll(UserBase):
    password: str


class BookPublic(BookBase):
    id: uuid.UUID


class BooksPublic(SQLModel):
    data: List[BookPublic]
    count: int


class BorrowedBook(SQLModel, table=True):
    __tablename__ = "borrowed_books"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    book_id: uuid.UUID = Field(foreign_key="books.id")
    borrow_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    period_in_days: int = Field(nullable=False)
    return_date: datetime
    user: User = Relationship(back_populates="borrowed_books")
    book: Book = Relationship(back_populates="borrowed_books")


class BorrowedBookCreate(SQLModel):

    book_id: uuid.UUID
    period_in_days: int = Field(ge=1)


class BorrowedBooksPublic(SQLModel):
    data: List[BorrowedBook]
    count: int


class TokenPayload(SQLModel):
    sub: str | None = None
    payload: UserPublic | None = None


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int
