from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

def setup_cors(app: FastAPI) -> None:
    if settings.debug:
        allowed_origins = ["*"] # For development we are allowing all origins
    else:
        allowed_origins = [
            settings.base_url,
            # Add base urls here for production.
        ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["*"],
        max_age=3600 # Caching for 1 hr.
    )

    print(f"CORS configured - Allowed origins: {allowed_origins}")