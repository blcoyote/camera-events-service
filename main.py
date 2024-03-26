import asyncio
from datetime import datetime
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from firebase.firebase import get_firebase_app
from lib.settings import get_settings
from loguru import logger
from database import  schema, database
from contextlib import asynccontextmanager
from tasks.event_polling import poll_for_new_events, check_for_stale_fcmtokens
from controllers import (
    download_controller,
    event_controller,
    fcm_controller,
    fcm_controllerV2,
    user_controller,
    event_controllerv2,
)

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

#Deprecated routes (username/password based oauth)
app.include_router(user_controller.router)
app.include_router(event_controller.router)
app.include_router(fcm_controller.router)
# Active routes (firebase auth)
app.include_router(download_controller.router)
app.include_router(event_controllerv2.router)
app.include_router(fcm_controllerV2.router)

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