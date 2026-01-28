"""
Application settings using Pydantic v2.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Intuit IAM credentials (optional - only needed when using provider="intuit")
    client_app_secret: str = Field(
        default="", description="Client application secret for authentication"
    )
    experience_id: str = Field(default="", description="Intuit experience ID")
    client_app_id: str = Field(default="", description="Client application ID")
    profile_id: str = Field(default="", description="Profile ID for authentication")

    # Pydantic v2 uses model_config instead of inner Config class
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore",
    }


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

