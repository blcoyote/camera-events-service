from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field
from loguru import logger
import os


@lru_cache()
def get_settings():
    return Settings() 

class Settings(BaseSettings):
    model_config = ConfigDict(extra="allow")
    app_name: str = Field("Frigate API")
    docs_url: str = Field(os.getenv("UVICORN_DOCS_LOCATION", ""))
    app_version: str = Field(os.getenv("UVICORN_APP_VERSION", ""))
    frigate_baseurl: str = Field(os.getenv("UVICORN_FRIGATE_BASEURL", ""))
    secret_key: str = Field(os.getenv("UVICORN_SECRET_KEY", ""))
    sqlalchemy_database_url: str = Field(os.getenv("UVICORN_DATABASE_URL", ""))
    web_url: str = Field(os.getenv("UVICORN_WEB_URL", ""))
    cameras: List[str] = Field(
        [
            "gavl_vest",
            "garage",
            "gavl_oest",
            "have",
            "rpiCamera",
            "stuen",
            "koekken",
            "reserve",
        ]
    )
