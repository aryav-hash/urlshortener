from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ShortenRequest(BaseModel):
    url: str
    custom_code: str | None = None
    expiry : int | None = None

class ShortenResponse(BaseModel):
    short_url: str
    code: str
    created_at: str | None = None
    expiry: str | None = None

@router.post("/api/shorten/", response_model=ShortenResponse)
async def shorten(req: ShortenRequest):
    return 404
