from pydantic import BaseModel, Field
from datetime import datetime

class ShortenURLResult(BaseModel):
    short_code: str = Field(..., description="The generated short code")
    already_exists: bool = Field(..., description="Presence of the url in the database")
    original_url: str = Field(..., description="The original long URL")
    short_url: str = Field(..., description="Shortened version of long URL")
    created_at: datetime | None = Field(None, description="When the URL was created")