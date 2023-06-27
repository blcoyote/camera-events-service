from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models import user
from database import schema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    return db.query(schema.User).filter(schema.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(schema.User).filter(schema.User.email == email).first()


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
