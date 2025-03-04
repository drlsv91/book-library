from fastapi import APIRouter
from app.api.routes import user
from app.api.routes import auth

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(user.router)
