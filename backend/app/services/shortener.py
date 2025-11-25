import string
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from app.db import queries
from app.schemas.shortener import ShortenURLResult
from better_profanity import profanity

profanity.load_censor_words()

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

# Below returns an is_valid(bool) and error_message(string) for validation
def validate_custom_code(custom_code: str) -> tuple[bool, str | None]:
    if len(custom_code) < 3:
        return False, "Custom code must be at least 3 characters long"
    
    if len(custom_code) > 15:
        return False, "Custom code must be at most 20 characters long"
    
    if not custom_code.isalnum():
        return False, "Custom code can only contain letters and numbers (a-Z, A-Z, 0-9)"
    
    if profanity.contains_profanity(custom_code.lower()):
        return False, "This custom code is not allowed"
    
    return True, None

async def shorten_url(
        db: AsyncSession, 
        url: str,
        custom_code: str | None = None,
        expiry_days: int | None = None
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
    
    if custom_code:
        is_valid, error_message = validate_custom_code(custom_code)
        if not is_valid:
            raise ValueError(error_message)
        
        check_for_existing_code = await queries.check_for_short_code(db, custom_code)
        if check_for_existing_code:
            raise ValueError(f"The entered code '{custom_code} is already in use.'")
        
        short_code = custom_code
    else:
        get_id = await queries.get_highest_id(db) + 1
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

    
    