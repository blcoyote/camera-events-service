from functools import lru_cache
from pydantic import BaseSettings
from loguru import logger
import os


@lru_cache()
def get_settings():
    return Settings() 

class Settings(BaseSettings):
    app_name: str = "Frigate API"
    docs_url: str = os.getenv("UVICORN_DOCS_LOCATION", "")
    app_version: str = os.getenv("UVICORN_APP_VERSION", "")
    frigate_baseurl: str = os.getenv("UVICORN_FRIGATE_BASEURL", "")
    secret_key: str = os.getenv("UVICORN_SECRET_KEY", "")
    sqlalchemy_database_url: str = os.getenv("UVICORN_DATABASE_URL", "")
    



