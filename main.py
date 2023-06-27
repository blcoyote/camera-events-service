from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from controllers import event_controller, user_controller
from lib.auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token
from lib.settings import get_settings
from loguru import logger
from lib.websockets import get_connection_manager
from sqlalchemy.orm import Session
from models.token import Token
from database import schema, database

schema.Base.metadata.create_all(bind=database.engine)

logger.remove(0)
logger.add(f"./log/apilog_{datetime.now().strftime('%Y-%m-%d')}.log", rotation="1 day",
           colorize=False, format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | <level>{message}</level>")

app = FastAPI(title=get_settings().app_name, version=get_settings().app_version, debug=False)
app.include_router(event_controller.router)
app.include_router(user_controller.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


manager = get_connection_manager()

@app.get("/application-configuration")
def app_config():
    return {}

@app.post("/token", response_model=Token)
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
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

