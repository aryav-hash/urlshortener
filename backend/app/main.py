from fastapi import FastAPI, Depends
import aioredis
from app.config import settings
from app.api import routes
from app.middleware import (
    setup_cors,
    setup_logging,
    setup_error_handlers
)

app = FastAPI()
redis_client = None

