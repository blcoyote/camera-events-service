from time import time
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models import user
from database import schema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    return db.query(schema.User).filter(schema.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(schema.User).filter(schema.User.email == email).first()

def get_user_by_id(db: Session, id: int):
    return db.query(schema.User).filter(schema.User.id == id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(schema.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: user.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = schema.User(username=user.username, email=user.email, full_name=user.full_name, hashed_password=hashed_password, disabled=True)
    # create_user as disabled by default
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_refresh_token(db: Session, token: str, username: str):
    db_token = schema.RefreshToken(token=token, username=username)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def find_refresh_token(db: Session, token: str):
    return db.query(schema.RefreshToken).filter(schema.RefreshToken.token == token).first()

def remove_refresh_token(db: Session, token: str):
    db.query(schema.RefreshToken).filter(schema.RefreshToken.token == token).delete()
    db.commit()

def store_fcm_token(db: Session, fcm_token:str):
    db_token = schema.FcmToken(fcmToken=fcm_token, lastUploadedEpoch=int(time.time()))
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def find_fcm_token(db: Session, fcm_token:str):
    return db.query(schema.FcmToken).filter(schema.FcmToken.fcmToken == fcm_token).first()

def get_stale_fcm_tokens(db: Session):
    return db.query(schema.FcmToken).filter(schema.FcmToken.lastUploadedEpoch < int(time.time()) - 60*60*24*7*30).all()

def delete_stale_fcm_tokens(db: Session):
    db.query(schema.FcmToken).filter(schema.FcmToken.lastUploadedEpoch < int(time.time()) - 60*60*24*7*30).delete()
    db.commit()