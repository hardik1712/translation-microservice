import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "Translation Microservice"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./translation_logs.db"
    
    # Google Translate settings
    GOOGLE_TRANSLATE_API_KEY: Optional[str] = None
    
    # Mock mode (when no API key is available)
    USE_MOCK_TRANSLATION: bool = True
    
    class Config:
        env_file = ".env"

def get_settings() -> Settings:
    return Settings()