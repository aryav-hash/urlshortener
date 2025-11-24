from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    database_connection: str
    debug: bool = False
    base_url: str = "http://localhost:5000" # This is the base url for the application
    secret_key: str = "dev-secret-key" # For setting up future session etc...

    @property
    def database_url(self) -> str:
        return (
            self.database_connection
            .replace("postgres://", "postgresql+asyncpg://")
            .replace("?sslmode=require", "")
        )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

@lru_cache()    
def get_settings() -> Settings:
    return Settings()

settings = get_settings()