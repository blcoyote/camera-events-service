from pydantic import BaseModel


class AppConfigModel(BaseModel):
    apiKey: str
    authDomain: str
    projectId: str
    storageBucket: str
    messagingSenderId: str 
    appId: str 
    measurementId: str 
    messagingKey: str 