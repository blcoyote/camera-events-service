from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from models.user import User, UserCreate, UserGet
from database import crud, database
from lib.auth import get_current_active_user
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_active_user)],
    responses={404: {"description": "Not found"}},
    deprecated=True
)


@router.get("/users/me", response_model=UserGet)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

@router.get("/users/", response_model=list[User])
def read_users( skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.post("/users/", response_model=UserGet)
def create_user(user: UserCreate, current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
