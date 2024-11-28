from time import time
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models import user
from database import schema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def store_fcm_token(db: Session, fcm_token:str):
    db_token = schema.FcmToken(fcmToken=fcm_token, lastUploadedEpoch=int(time()))
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def update_fcm_token_last_uploaded(db: Session, fcm_token:str):
    db_token = db.query(schema.FcmToken).filter(schema.FcmToken.fcmToken == fcm_token).first()
    db_token.lastUploadedEpoch = int(time())
    db.commit()
    db.refresh(db_token)
    return db_token

def find_fcm_token(db: Session, fcm_token:str):
    return db.query(schema.FcmToken).filter(schema.FcmToken.fcmToken == fcm_token).first()

def get_stale_fcm_tokens(db: Session):
    return db.query(schema.FcmToken).filter(schema.FcmToken.lastUploadedEpoch < int(time()) - 60*60*24*7*4).all()

def delete_stale_fcm_tokens(db: Session):
    db.query(schema.FcmToken).filter(schema.FcmToken.lastUploadedEpoch < int(time()) - 60*60*24*7*4).delete()
    db.commit()