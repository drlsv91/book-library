import uuid
from sqlmodel import (
    Field,
    Relationship,
    SQLModel,
)

from typing import List
from datetime import datetime
from pydantic import EmailStr


class Book(SQLModel, table=True):
    __tablename__ = "books"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(index=True, max_length=255)
    author: str = Field(index=True, max_length=255)
    published_date: datetime = Field(default_factory=datetime.now)
    publisher: str = Field(max_length=255)
    is_available: bool = Field(default=False)
    borrowed_books: List["BorrowedBook"] = Relationship(back_populates="book")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    first_name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    email: EmailStr = Field(unique=True, index=True)
    borrowed_books: List["BorrowedBook"] = Relationship(back_populates="book")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class BorrowedBook(SQLModel, table=True):
    __tablename__ = "borrowed_books"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    book_id: int = Field(foreign_key="books.id")
    borrow_date: datetime = Field(default_factory=datetime.now)
    return_date: datetime = Field()

    user: User = Relationship(back_populates="borrowed_books")
    book: Book = Relationship(back_populates="borrowed_books")
