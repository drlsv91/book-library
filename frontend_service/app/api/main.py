from fastapi import APIRouter
from app.api.routes import user, book

api_router = APIRouter()

api_router.include_router(user.router)
api_router.include_router(book.router)
