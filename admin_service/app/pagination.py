from typing import Generic, TypeVar, List
from sqlmodel import SQLModel

T = TypeVar("T")


class PaginatedResponse(SQLModel, Generic[T]):
    data: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
