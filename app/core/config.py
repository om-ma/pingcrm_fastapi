from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv
import os

# Load the environment variables from .env file
load_dotenv(override=True)

class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()

# Debug print to verify the database URL
print(f"Loaded DATABASE_URL: {settings.DATABASE_URL}")
