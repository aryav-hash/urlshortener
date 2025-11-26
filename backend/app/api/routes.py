from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.resources import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.logic import get_db
from app.db import queries
from app.services import shortener
from app.schemas.shortener import ShortenRequest, ShortenResponse, ErrorResponse
from app.config import settings

router = APIRouter()

@router.post(
    "/api/shorten",
    response_model=ShortenResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request or validation error"},
        409: {"model": ErrorResponse, "description": "Custom code already taken"}
    },
    tags=["URL Shortening"]
)
async def create_short_url(
    request: ShortenRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await shortener.shorten_url(
            db=db,
            url=str(request.url),
            custom_code=request.custom_code,
            expiry_days=request.expiry_days
        )

        if result.already_exists:
            message = "This URL has already been shortened"
            status_code = status.HTTP_200_OK
        elif request.custom_code:
            message = f"Custom short URL created successfully"
        else:
            message = "Short URL created successfully"

        return ShortenResponse(
            short_url=result.short_url,
            code=result.short_code,
            original_url=result.original_url,
            created_at=result.created_at.isoformat() if result.created_at else None,
            expiry=result.expiry.isoformat() if result.expiry else None,
            already_exists=result.already_exists,
            message=message
        )
    except ValueError as e:
        error_message = str(e)

        if "already in use" in error_message.lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": "CustomCodeTaken",
                    "detail": error_message
                }
            )
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "ValidationError",
                "detail": error_message
            }
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "InternalServerError",
                "detail": "An unexpected error occurred while creating the short URL"
            }
        )