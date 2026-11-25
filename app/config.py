from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    redis_url: str = "redis://localhost:6379/0"
    velocity_window_seconds: int = 300
    velocity_limit: int = 5


@lru_cache
def get_settings() -> Settings:
    return Settings()
