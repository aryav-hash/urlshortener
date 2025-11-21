import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv
import os

load_dotenv()

async def test_connection():
    db_url = os.getenv("DATABASE_CONNECTION")
    async_db_url = db_url.replace("postgres://", "postgresql+asyncpg://").replace("?sslmode=require", "")
    try:
        engine = create_async_engine(async_db_url, echo=True, connect_args={"ssl": "require"})
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT version();"))
            version = result.fetchone()
            print("\nCONNECTION SUCCESSFUL!")
            print(f"\nDatabase version: {version[0]}")
        
        await engine.dispose()

    except Exception as e:
        print(f"\n CONNECTION FAILED!")
        print(f"Error: {e}\n")

if __name__ == "__main__":
    asyncio.run(test_connection())
