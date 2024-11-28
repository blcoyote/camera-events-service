import asyncio
from datetime import datetime
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from firebase.firebase import get_firebase_app
from lib.settings import get_settings
from loguru import logger
from contextlib import asynccontextmanager
from tasks.event_polling import poll_for_new_events
from controllers import (
    download_controller,
    fcm_controller,
    notification_controller,
    event_controller,
)

logger.add(f"./logs/apilog_{datetime.now().strftime('%Y-%m-%d')}.log", rotation="1 day",
           colorize=False, format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | <level>{message}</level>")

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(poll_for_new_events())
    yield

app = FastAPI(
    title=get_settings().app_name,
    version=get_settings().app_version,
    debug=False,
    docs_url=get_settings().docs_url,  # Disable docs (Swagger UI)
    redoc_url=None,  # Disable redoc
    lifespan=lifespan,
)

# CORS - change this when frontend is intefrated
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Active routes (firebase auth)
app.include_router(download_controller.router)
app.include_router(event_controller.router)
app.include_router(fcm_controller.router)
app.include_router(notification_controller.router)



logger.info("Starting Frigate API...")
firebase_App = get_firebase_app()

background_tasks = BackgroundTasks()
