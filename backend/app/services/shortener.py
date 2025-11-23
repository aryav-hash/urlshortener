import string
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.logic import AsyncSessionLocal
from app.db import queries

# URL Shortener
# Let's try to generate a shortened url from a big url like that of an amazon product.
def generate_url(index: int) -> str: 
    characters = string.digits + string.ascii_lowercase + string.ascii_uppercase

    if index == 0:
        return characters[0]

    result = []
    while index > 0:
        rem = index % 62
        result.append(characters[rem])
        index = index // 62
    
    return ''.join(reversed(result))

async def shorten_url(db: AsyncSession, url: str): 
    exists = await queries.check_if_url_exists_in_db(db, url)

    if exists is None:
        highest_id = await queries.get_highest_id(db)
        print(highest_id)
    

