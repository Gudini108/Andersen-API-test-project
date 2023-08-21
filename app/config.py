"""Enviroment configuration"""

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Database settings"""
    db_url: str = Field(..., env='DATABASE_URL')


settings = Settings()
