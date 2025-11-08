from fastapi import FastAPI, Depends
import aioredis
from app.config import settings
from app.api import routes

app = FastAPI()
redis_client = None

