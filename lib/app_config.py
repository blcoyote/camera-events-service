from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import  Field
import os

@lru_cache()
def get_app_config():
    return FrontEndConfig() 

class FrontEndConfig(BaseSettings):
    apiKey: str = Field(os.getenv("UVICORN_FIREBASE_APIKEY", ""))
    authDomain: str = Field(os.getenv("UVICORN_AUTHDOMAIN", ""))
    projectId: str = Field(os.getenv("UVICORN_PROJECTID", ""))
    storageBucket: str = Field(os.getenv("UVICORN_STORAGEBUCKET", ""))
    messagingSenderId: str = Field(os.getenv("UVICORN_MESSAGESENDERID", ""))
    appId: str = Field(os.getenv("UVICORN_APPID", ""))
    measurementId: str = Field(os.getenv("UVICORN_MEASUREMENTID", ""))
    messagingKey: str = Field(os.getenv("UVICORN_MESSAGINGKEY", ""))