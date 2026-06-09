from pydantic_settings import BaseSettings
from typing import Literal
from pathlib import Path

env_path = Path(__file__).resolve().parents[3] / ".env"

class Settings(BaseSettings):
    AI_PROVIDER: Literal["groq", "ollama"] = "groq"
    GROQ_API_KEY: str = ""
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_KEY: str = ""
    DB_PASSWORD: str = ""
    SECRET_KEY: str = "dev-secret-key"
    ENVIRONMENT: Literal["development", "production"] = "development"

    class Config:
        env_file = str(env_path)
        extra = "ignore"

settings = Settings()