import string
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from app.db import queries
from app.schemas.shortener import ShortenURLResult

# URL Shortener
# Let's try to generate a shortened url from a big url like that of an amazon product.
def generate_short_url(index: int) -> str: 
    characters = string.digits + string.ascii_lowercase + string.ascii_uppercase

    if index == 0:
        return characters[0]

    result = []
    while index > 0:
        rem = index % 62
        result.append(characters[rem])
        index = index // 62
    
    return ''.join(reversed(result))

async def shorten_url(
        db: AsyncSession, 
        url: str,
        custom_code: str | None = None,
        expiry_days: int | None = None
) -> ShortenURLResult: 
    exists = await queries.check_if_url_exists_in_db(db, url)

    if exists:
        return ShortenResult(
            short_code=exists.short_code,
            already_exists=True,
            original_url=exists.original_url,
            short_url="will_update_later",
            created_at=exists.created_at,
            expiry=exists.expiry 
        )
        
    
    