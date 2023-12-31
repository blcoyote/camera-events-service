from sqlalchemy import Boolean, Column, Integer, String
from .database import Base 


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    disabled = Column(Boolean, default=True, nullable=False)



class  RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    token = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, index=True, nullable=False)

class FcmToken(Base):
    __tablename__ =  "fcm_tokens"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    fcmToken = Column(String, unique=True, index=True, nullable=False)
    lastUploadedEpoch = Column(Integer, nullable=False)
