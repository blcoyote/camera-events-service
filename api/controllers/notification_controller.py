import io
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from loguru import logger
from database.redis_datastore import get_snapshot_id

from tasks.event_tasks import  get_placeholder, get_snapshot
from starlette.responses import StreamingResponse

router = APIRouter(
    prefix="/api/v2/attachments",
    tags=["v2/attachments"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("/notification/{image_token}", status_code=200)
async def read_event_latest(image_token: str):

    event_id = get_snapshot_id(image_token)
    logger.info(f"Getting snapshot for event {event_id}")
    try:
        if event_id is not None:
            return StreamingResponse(io.BytesIO(get_snapshot(event_id)), media_type="image/jpg")
        return StreamingResponse(io.BytesIO(get_placeholder()), media_type="image/png")
    except Exception as e:
        logger.error(f"Error getting snapshot: {e}")



