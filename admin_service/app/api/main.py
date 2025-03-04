from app.api.routes import user, book
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(user.router)
api_router.include_router(book.router)
