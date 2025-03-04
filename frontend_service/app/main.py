from fastapi import FastAPI
from app.api.main import api_router
from app.core.config import settings
from starlette.middleware.cors import CORSMiddleware
from app.events import listen_for_events
from threading import Thread

app = FastAPI(title=settings.PROJECT_NAME)

if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        # allow_origins=settings.all_cors_origins,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Start listeners in a separate thread
Thread(target=listen_for_events, daemon=True).start()

app.include_router(api_router, prefix=settings.API_V1_STR)
