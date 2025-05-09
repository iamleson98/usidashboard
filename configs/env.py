from functools import lru_cache
import os
from pydantic_settings import BaseSettings
import sys

@lru_cache
def get_env_filename():
    runtime_env = os.getenv("ENV")
    if not runtime_env:
        print(sys.argv)
        if "--dev" in sys.argv:
            runtime_env = "dev"
    return f".env.{runtime_env}" if runtime_env else ".env"


class EnvironmentSettings(BaseSettings):
    API_VERSION: str
    APP_NAME: str
    DB_HOST: str
    DB_NAME: str
    DB_PASSWORD: str
    DB_PORT: int
    DB_USERNAME: str
    DEBUG_MODE: bool
    AUTHORS: str
    DATA_CRAWLER_INTERVAL_MINS: int
    ALLOWED_ORIGINS: str

    class Config:
        env_file = get_env_filename()
        env_file_encoding = "utf-8"

@lru_cache
def get_environment_variables():
    return EnvironmentSettings()

