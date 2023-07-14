import asyncio
from loguru import logger
from datetime import datetime, timedelta
from database import database
from database.crud import delete_stale_fcm_tokens, get_stale_fcm_tokens
from firebase.firebase import send_topic_push
from tasks.event_tasks import get_events
from models.event_model import CameraEventQueryParams, CameraNotification, WsEventType, WebsocketEvent

POLLING_INTERVAL = 30

async def poll_for_new_events():
    aftertime = datetime.now()- timedelta(seconds = POLLING_INTERVAL)
    while True:
        #logger.info(f"Polling for new events from {aftertime}")
        params = CameraEventQueryParams()
        params.after=int(aftertime.timestamp())
        params.limit=200

        aftertime = datetime.now() #next run

        events = get_events(params)
        

        if len(events) > 0:
            logger.info(f"Found {len(events)} events. Pushing to clients")
            for event in events:
                try:
                    #await manager.broadcast(wsEvent.json())
                    send_topic_push(event)
                except Exception as e:
                    logger.error(f"Error sending event to firebase: {e}")
        
        await asyncio.sleep(POLLING_INTERVAL)

async def check_for_stale_fcmtokens():
    await asyncio.sleep(60)
    while True:
        logger.info(f"Checking for stale FCM tokens")
        try:
            get_stale_fcm_tokens(database.SessionLocal())
        except Exception as e:
            logger.error(f"Error deleting stale FCM tokens: {e}")
            
        await asyncio.sleep(60*60*24*7) # 1 week