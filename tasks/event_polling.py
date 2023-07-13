import asyncio
from loguru import logger
from datetime import datetime, timedelta
from firebase.firebase import send_topic_push
from tasks.event_tasks import get_events
from lib.websockets import get_connection_manager
from models.event_model import CameraEventQueryParams, CameraNotification, WsEventType, WebsocketEvent

POLLING_INTERVAL = 30

manager = get_connection_manager()

async def poll_for_new_events():
    
    while True:
        #logger.info("Polling for new events...")
        params = CameraEventQueryParams()
        aftertime = datetime.now()- timedelta(seconds = POLLING_INTERVAL)
        params.after=int(aftertime.timestamp())
        params.limit=2000

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
