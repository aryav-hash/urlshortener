from pydantic import BaseModel, Field, HttpUrl, validator
from datetime import datetime

class ShortenRequest(BaseModel):
    url: HttpUrl = Field(
        ...,
        description="URL to shorten"
    )
    custom_code: str | None = Field(
        None, 
        min_length=3,
        max_length=15,
        description="custom short code provided by the user (3-15 in length and alphanumeric)"
    )
    expiry_days: int | None = Field(
        None,
        gt=0,
        le=365,
        description="Optional expiry days (1-365). Defaults to 10 days if not provided."
    )

    @validator('custom_code')
    def validate_custom_code(cls, v):
        if v is None:
            return v
        
        if not v.isalnum():
            raise ValueError('Custom code must contain only letters and numbers')
        
        return v

# Need to look at certain things here
class ShortenResponse(BaseModel): # Response schema after shortening the URL.
    short_url: str = Field(..., description="The complete shortened URL")
    code: str = Field(..., description="The short code")
    original_url: str = Field(..., description="The original URL")
    created_at: str | None = Field(None, description="Creation timestamp")
    expiry: str | None = Field(None, description="Expiration timestamp")
    already_exists: bool = Field(..., description="Whether URL was already shortened")
    message: str = Field(..., description="Some message for the user")

class ShortenURLResult(BaseModel):
    short_code: str = Field(..., description="The generated short code")
    already_exists: bool = Field(..., description="Presence of the URL in the database")
    original_url: str = Field(..., description="The original long URL")
    short_url: str = Field(..., description="Shortened version of long URL")
    created_at: datetime | None = Field(None, description="When the URL was created")
    expiry: datetime | None = Field(None, description="When the URL expires")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error type")
    detail: str = Field(..., description="Details of the error message")

    class Config:
        json_schema_type = {
            "example": {
                "error": "ValidationError",
                "detail": "Custom code must be at least 3 characters long"
            }
        }