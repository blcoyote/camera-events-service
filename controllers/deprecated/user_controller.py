from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models.user import User, UserCreate, UserGet
from database import crud, database
from lib.auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, get_current_active_user
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from lib.auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token,  refresh_access_token
from sqlalchemy.orm import Session
from models.user import User
from models.token import Token
from database import crud,  database


router = APIRouter(
    prefix="",
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

@router.post("/token", response_model=Token, deprecated=True)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(database.get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(db, data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token[0], "refresh_token":access_token[1], "token_type": "bearer"}


@router.post("/token/refresh", response_model=Token, deprecated=True)
async def refresh_token(
    token: str, 
    user: str,
    db: Session = Depends(database.get_db)
    ):
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = refresh_access_token(db, refresh_token=token,
        data={"sub": user}, expires_delta=access_token_expires
    )
    return {"access_token": access_token[0], "refresh_token":access_token[1], "token_type": "bearer"}


