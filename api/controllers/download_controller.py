import io
from fastapi import APIRouter, Depends
from firebase.auth import verify_url_token
from tasks.event_tasks import get_clip, get_latest, get_snapshot
from starlette.responses import StreamingResponse

router = APIRouter(
    prefix="/api/v2/downloads",
    tags=["v2/downloads"],
    dependencies=[Depends(verify_url_token)],
    responses={404: {"description": "Not found"}},
)


@router.get("/{event_id}/snapshot.jpg", status_code=200)
async def read_event_snapshot(event_id: str):
    return StreamingResponse(
        io.BytesIO(get_snapshot(event_id)),
        media_type="image/jpg",
        headers={
            "Content-Disposition": f"attachment; filename=snapshot-{event_id}.jpg",
        },
    )


@router.get("/{camera}/latest.jpg", status_code=200)
async def read_event_latest(camera: str):
    return StreamingResponse(
        io.BytesIO(get_latest(camera)),
        media_type="image/jpg",
        headers={
            "Content-Disposition": f"attachment; filename=latest-{camera}.jpg",
        },
    )


@router.get("/{event_id}/clip.mp4", status_code=200)
async def read_event_clip(event_id: str):
    return StreamingResponse(
        io.BytesIO(get_clip(event_id)),
        media_type="video/mp4",
        headers={
            "Content-Disposition": f"attachment; filename=clip-{event_id}.mp4",
        },
    )
