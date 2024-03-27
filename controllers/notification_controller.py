import io
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from database.redis_datastore import get_snapshot_id
from firebase.auth import verify_url_token
from lib.settings import get_settings
from tasks.event_tasks import get_clip, get_latest, get_snapshot
from starlette.responses import StreamingResponse

router = APIRouter(
    prefix="/api/v2/attachments",
    tags=["v2/attachments"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


def invalid_image():
    return RedirectResponse(url=f"https://{get_settings().web_url}/pwa-192x192.png")


@router.get("/notification/{image_token}", status_code=200)
async def read_event_latest(image_token: str):
    try:
        event_id = get_snapshot_id(image_token)
        if event_id is None:
            return invalid_image()
        return StreamingResponse(io.BytesIO(event_id), media_type="image/jpg")
    except:
        return invalid_image()

