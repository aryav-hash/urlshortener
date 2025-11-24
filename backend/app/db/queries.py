from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import URL 
from datetime import datetime

async def check_if_url_exists_in_db(db: AsyncSession, original_url: str) -> URL | None:
    result = await db.execute(
        select(URL).where(URL.original_url == original_url)
    )
    url_record = result.scalar_one_or_none()
    return url_record if url_record is not None else None

async def get_highest_id(db: AsyncSession) -> int: 
    result = await db.execute(
        select(func.max(URL.id))
    )
    max_id = result.scalar()
    return max_id if max_id is not None else 0

async def insert_url(
        db: AsyncSession,
        original_url: str,
        short_code: str,
        expiry: datetime | None = None
) -> URL:
    
    new_entry = URL(
        original_url = original_url,
        short_code=short_code,
        created_at=datetime.utcnow(),
        expiry=expiry,
    )
    db.add(new_entry)
    await db.commit()
    await db.refresh(new_entry)
    return new_entry