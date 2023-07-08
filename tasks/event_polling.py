import asyncio
from loguru import logger
from datetime import datetime, timedelta
from tasks.event_tasks import get_events
from lib.websockets import get_connection_manager
from models.event_model import CameraEventQueryParams, CameraNotification, WsEventType, WebsocketEvent


manager = get_connection_manager()

async def poll_for_new_events():
    
    while True:
        logger.info("Polling for new events...")
        params = CameraEventQueryParams()
        aftertime = datetime.now()- timedelta(seconds = 60)
        params.after=int(aftertime.timestamp())

        events = get_events(params)

        if len(events) > 0:
            logger.info(f"Found {len(events)} events. Pushing to websocket clients")
            for event in events:
                
                cameraNotification = CameraNotification(id=event.id, camera=event.camera)
                wsEvent = WebsocketEvent(type=WsEventType.MOVEMENT, content=cameraNotification)
                try:
                    await manager.broadcast(wsEvent.json())
                except Exception as e:
                    logger.error(f"Error broadcasting event to websocket clients: {e}")

        await asyncio.sleep(60)
