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
) -> ShortenURLResult: 
    exists = await queries.check_if_url_exists_in_db(db, url)

    if exists:
        return ShortenURLResult(
            short_code=exists.short_code,
            already_exists=True,
            original_url=exists.original_url,
            short_url="will_update_later",
            created_at=exists.created_at,
            expiry=exists.expiry 
        )
    
    get_id = queries.get_highest_id(db)+1
    hashed_value = generate_short_url(get_id) 
    # Currently not adding any expiry date
     
    new_entry = await queries.insert_url(
        db,
        original_url = url,
        short_code = hashed_value,
    )

    return ShortenURLResult(
        short_code = new_entry.short_code,
        already_exists=False,
        original_url=new_entry.original_url,
        short_url=f"will_update_later",
        created_at=new_entry.created_at,
    )

    
    