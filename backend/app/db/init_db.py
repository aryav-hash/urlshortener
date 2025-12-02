import asyncio
from app.db.logic import engine
from app.db.base import Base
from app.models import URL

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("Tables created successfully!\n")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(create_tables())