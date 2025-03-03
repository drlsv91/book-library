from fastapi import FastAPI
from app.core.config import settings
from starlette.middleware.cors import CORSMiddleware
from app.api.main import api_router


app = FastAPI(
    title=settings.PROJECT_NAME,
)


if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(api_router, prefix=settings.API_V1_STR)
