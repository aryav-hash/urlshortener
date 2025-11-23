from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import URL 

async def check_if_url_exists_in_db(db: AsyncSession, original_url: str) -> bool:
    result = await db.execute(
        select(URL).where(URL.original_url == original_url)
    )
    url_record = result.scalar_one_or_none()
    return url_record is not None

