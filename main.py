import asyncio
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, WebSocket, WebSocketDisconnect, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from controllers import event_controller, user_controller
from lib.auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_active_user, get_current_user
from lib.settings import get_settings
from loguru import logger
from lib.websockets import get_connection_manager
from sqlalchemy.orm import Session
from models.token import Token
from database import schema, database
from tasks.event_polling import poll_for_new_events

schema.Base.metadata.create_all(bind=database.engine)

logger.add(f"./logs/apilog_{datetime.now().strftime('%Y-%m-%d')}.log", rotation="1 day",
           colorize=False, format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | <level>{message}</level>")

app = FastAPI(
    title=get_settings().app_name, 
    version=get_settings().app_version, 
    debug=False,
    docs_url=get_settings().docs_url, # Disable docs (Swagger UI)
    redoc_url=None, # Disable redoc
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

manager = get_connection_manager()

background_tasks = BackgroundTasks()

@app.on_event('startup')
async def app_startup():
    asyncio.create_task(poll_for_new_events())


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
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}




@app.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str, db: Session = Depends(database.get_db)):
    user: schema.User
    try:
        user = await get_current_user(token, db)
        logger.info(f"User {user.username} connected to websocket")
    except Exception as e:
        logger.info(f"Invalid token: {token}, exception: {e}")
        await websocket.close(code=401, reason="Invalid token")
        raise(HTTPException(status_code=401, detail="Invalid token"))

    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Received data from user: {data}")

            #TODO: do subscription magic?

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Hello everyone")
  