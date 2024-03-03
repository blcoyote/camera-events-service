import asyncio
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, WebSocket, WebSocketDisconnect, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from controllers import event_controller, user_controller
from firebase.firebase import get_firebase_app, subscribe_topic, send_topic_push
from lib.auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_user, refresh_access_token
from lib.settings import get_settings
from loguru import logger
from sqlalchemy.orm import Session
from models.user import User
from models.token import Token
from database import crud, schema, database
from contextlib import asynccontextmanager
from tasks.event_polling import poll_for_new_events, check_for_stale_fcmtokens

schema.Base.metadata.create_all(bind=database.engine)


logger.add(f"./logs/apilog_{datetime.now().strftime('%Y-%m-%d')}.log", rotation="1 day",
           colorize=False, format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | <level>{message}</level>")
@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(poll_for_new_events())
    asyncio.create_task(check_for_stale_fcmtokens())
    yield


app = FastAPI(
    title=get_settings().app_name,
    version=get_settings().app_version,
    debug=False,
    docs_url=get_settings().docs_url,  # Disable docs (Swagger UI)
    redoc_url=None,  # Disable redoc
    lifespan=lifespan,
)
app.include_router(event_controller.router)
app.include_router(user_controller.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
logger.info("Starting Frigate API...")
firebase_App = get_firebase_app()


background_tasks = BackgroundTasks()


@app.get("/application-configuration")
async def app_config():
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
    access_token = create_access_token(db, data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token[0], "refresh_token":access_token[1], "token_type": "bearer"}


@app.post("/token/refresh", response_model=Token)
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


@app.post("/fcm", status_code=200)
async def register_fcm(token: str, current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(database.get_db)):

    try:
        existing_token = crud.find_fcm_token(db=db, fcm_token=token)

        if existing_token != None:
            logger.info(f"FCM token already registered for user {current_user.username}")

            if existing_token.lastUploadedEpoch < int(datetime.now().timestamp()) - 60*60*24*7*2:
                subscribe_topic(token)
                crud.update_fcm_token_last_uploaded(db=db, fcm_token=token)
                logger.info(f"FCM token last uploaded more than 2 weeks ago. Re-subscribing to topic")

        else:
            logger.info(f"Registering FCM token for user {current_user.username}")
            subscribe_topic(token)
            crud.store_fcm_token(db=db, fcm_token=token)

    except Exception as e:
        logger.error(f"Failed to handle fcm token: {e}")
