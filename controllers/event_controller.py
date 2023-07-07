import io
from typing import List
from fastapi import APIRouter, Depends
from loguru import logger
from lib.websockets import get_connection_manager
from tasks.event_tasks import get_events, get_snapshot
from models.event_model import CameraEvent
from lib.auth import get_current_active_user
from starlette.responses import StreamingResponse

manager = get_connection_manager()

router = APIRouter(
    prefix="/events",
    tags=["events"],
    dependencies=[Depends(get_current_active_user)],
    responses={404: {"description": "Not found"}},
)


@router.get("/" , response_model=List[CameraEvent], status_code=200, )
async def read_events():
    return get_events()

@router.get("/{event_id}" , response_model=CameraEvent, status_code=200)
async def read_event(event_id: str):
    return get_events(id=event_id)

@router.get("/{event_id}/snapshot.jpg", status_code=200)
async def read_event_snapshot(event_id: str):
    return StreamingResponse(io.BytesIO(get_snapshot(event_id)), media_type="image/png") 

