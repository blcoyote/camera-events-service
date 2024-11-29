from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field
import os


@lru_cache()
def get_settings():
    return Settings() 

class Settings(BaseSettings):
    model_config = ConfigDict(extra="allow")
    app_name: str = Field("Frigate API")
    docs_url: str = Field(os.getenv("UVICORN_DOCS_URL", ""))
    app_version: str = Field(os.getenv("UVICORN_APP_VERSION", ""))
    frigate_baseurl: str = Field(os.getenv("UVICORN_FRIGATE_BASEURL", ""))
    web_url: str = Field(os.getenv("UVICORN_WEB_URL", ""))
    redis_host: str = Field(os.getenv("UVICORN_REDIS_URL", ""))
    redis_password: str = Field(os.getenv("UVICORN_REDIS_PASSWORD", ""))
    cameras: List[str] = Field(
        [
            "gavl_vest",
            "garage",
            "gavl_oest",
            "have",
            "stuen",
            "koekken",
            "reserve",
        ]
    )
