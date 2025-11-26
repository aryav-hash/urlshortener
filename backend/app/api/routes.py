from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.resources import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.logic import get_db
from app.db import queries
from app.services import shortener
from app.schemas.shortener import ShortenRequest, ShortenResponse, ErrorResponse
from app.config import settings

router = APIRouter()
