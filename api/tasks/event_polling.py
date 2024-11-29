import asyncio
from typing import List
from loguru import logger
from datetime import datetime, timedelta
from firebase.firebase import send_multiple_topic_push, send_topic_push
from tasks.event_tasks import get_events
from models.event_model import CameraEvent, CameraEventQueryParams

POLLING_INTERVAL = 30

@logger.catch()
async def poll_for_new_events():
    while True:
        await fetch_and_process_events()
        await asyncio.sleep(POLLING_INTERVAL)

async def fetch_and_process_events():
    aftertime = datetime.now() - timedelta(seconds=POLLING_INTERVAL)
    params = CameraEventQueryParams()
    params.after = int(aftertime.timestamp())
    params.limit = 20

    aftertime = datetime.now()  # next run
    events: List[CameraEvent] = []

    try:
        events = get_events(params)
        # logger.info(f"Got {len(events)} events from api")
        
        await process_events(events)
    except Exception as e:
        logger.error(f"Error getting events from api: {e}")

async def process_events(events: List[CameraEvent]):
    try:
        if len(events) == 1:
            send_topic_push(events[0])
        elif len(events) > 1:
            logger.info(f"Found {len(events)} events. Pushing to clients")
            send_multiple_topic_push(events)
    except Exception as e:
        logger.error(f"Error sending event to firebase: {e}")