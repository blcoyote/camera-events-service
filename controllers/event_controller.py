import io
from typing import List
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from lib.settings import get_settings
from lib.websockets import get_connection_manager
from tasks.event_tasks import get_clip, get_events, get_latest, get_snapshot, get_event
from models.event_model import CameraEvent, CameraEventQueryParams
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
async def read_events(params: CameraEventQueryParams = Depends()):
    return get_events(params)

@router.get("/cameras", response_model=List[str], status_code=200)
async def read_camera_list():
    return get_settings().cameras

@router.get("/{event_id}" , response_model=CameraEvent, status_code=200)
async def read_event(event_id: str):
    return get_event(id=event_id)

@router.get("/{event_id}/snapshot.jpg", status_code=200)
async def read_event_snapshot(event_id: str):
    return StreamingResponse(io.BytesIO(get_snapshot(event_id)), media_type="image/jpg") 

@router.get("/{camera}/latest.jpg", status_code=200)
async def read_event_latest(camera: str):
    return StreamingResponse(io.BytesIO(get_latest(camera)), media_type="image/jpg") 

@router.get("/{event_id}/clip.mp4", status_code=200)
async def read_event_clip(event_id: str):
    return StreamingResponse(io.BytesIO(get_clip(event_id)), media_type="video/mp4") 


