import asyncio
from typing import List
from loguru import logger
from datetime import datetime, timedelta
from database import database
from database.crud import delete_stale_fcm_tokens, get_stale_fcm_tokens
from firebase.firebase import send_multiple_topic_push, send_topic_push
from tasks.event_tasks import get_events
from models.event_model import CameraEvent, CameraEventQueryParams, CameraNotification, WsEventType, WebsocketEvent

POLLING_INTERVAL = 30


async def poll_for_new_events():
    while True:
        aftertime = datetime.now() - timedelta(seconds=POLLING_INTERVAL)
        # logger.info(f"Polling for new events from {aftertime.timestamp()}")
        params = CameraEventQueryParams()
        params.after=int(aftertime.timestamp())
        params.limit = 20

        aftertime = datetime.now() #next run
        events: List[CameraEvent] = []

        try:
            events = get_events(params)
            logger.info(f"Got {len(events)} events from api")
        except Exception as e:
            logger.error(f"Error getting events from api: {e}")

        if len(events) == 1:
            logger.info(f"Found event. Pushing to clients")
            for event in events:
                try:
                    send_topic_push(event)
                except Exception as e:
                    logger.error(f"Error sending event to firebase: {e}")
        elif len(events) > 1:
            logger.info(f"Found {len(events)}  events. Pushing to clients")
            try:
                send_multiple_topic_push(events)
            except Exception as e:
                logger.error(f"Error sending event to firebase: {e}")

        await asyncio.sleep(POLLING_INTERVAL)


async def check_for_stale_fcmtokens():
    await asyncio.sleep(600)
    while True:
        logger.info(f"Checking for stale FCM tokens")
        try:
            delete_stale_fcm_tokens(database.SessionLocal())
        except Exception as e:
            logger.error(f"Error deleting stale FCM tokens: {e}")

        await asyncio.sleep(60*60*24*7) # 1 week
