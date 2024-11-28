from sqlalchemy import Boolean, Column, Integer, String
from .database import Base 

class FcmToken(Base):
    __tablename__ =  "fcm_tokens"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    fcmToken = Column(String, unique=True, index=True, nullable=False)
    lastUploadedEpoch = Column(Integer, nullable=False)
