import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    _db_url = os.getenv("DATABASE_CONNECTION")
    DATABASE_URL: str = _db_url.replace("postgres://", "postgresql+asyncpg://").replace("sslmode=require", "") if _db_url else None

settings = Settings()