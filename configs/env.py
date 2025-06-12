from functools import lru_cache
import os
from pydantic_settings import BaseSettings

@lru_cache
def get_env_filename():
    runtime_env = os.getenv("ENV")
    return f".env.dev"


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
    DATA_CRAWLER_INTERVAL_SECS: int
    REAL_TIME_REPORT_INTERVAL_SECS: int
    ALLOWED_ORIGINS: str
    REDIS_URL: str
    HIK_VISION_USER_NAME: str
    HIK_VISION_PASSWORD: str
    HIK_VISION_URL: str

    class Config:
        env_file = get_env_filename()
        env_file_encoding = "utf-8"

@lru_cache
def get_environment_variables():
    return EnvironmentSettings()


env = get_environment_variables()
