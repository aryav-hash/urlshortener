from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache

class Settings(BaseSettings):
    database_connection: str = Field(..., description="PostgreSQL connection string")
    debug: bool = Field(False, description="Enable debug mode")
    base_url: str = Field("http://localhost:5000", description="Base URL for shortened links") # This is the base url for the application
    secret_key: str = "dev-secret-key" # For setting up future sessions etc...

    # Configuration for redis
    redis_host: str = Field("localhost", description="Redis host")
    redis_port: int = Field(6379, description="Redis port")
    redis_db: int = Field(0, description="Redis database number") # redis has 16 databases(0-15)
    redis_cache_ttl: int = Field(3600, description="Cache TTL in seconds")

    @property
    def database_url(self) -> str:
        return (
            self.database_connection
            .replace("postgres://", "postgresql+asyncpg://")
            .replace("?sslmode=require", "")
        )
    
    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

@lru_cache()    
def get_settings() -> Settings:
    return Settings()

settings = get_settings()