from routes import login, user
from fastapi import APIRouter


api_router = APIRouter()

api_router.include_router(login.router)
api_router.include_router(user.router)
