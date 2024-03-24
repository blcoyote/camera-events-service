from datetime import datetime
from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy.orm import Session
from database import crud, database
from firebase.auth import verify_url_token
from firebase.firebase import subscribe_topic

router = APIRouter(
    prefix="/api/v2",
    tags=["v2/fcm"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/fcm", status_code=200)
async def register_fcm(
    fcm_token: str,
    db: Session = Depends(database.get_db),
    token: str = Depends(verify_url_token),
):
    try:
        existing_token = crud.find_fcm_token(db=db, fcm_token=fcm_token)
        if existing_token != None:
            if (
                existing_token.lastUploadedEpoch
                < int(datetime.now().timestamp()) - 60 * 60 * 24 * 7 * 2
            ):
                subscribe_topic(fcm_token)
                crud.update_fcm_token_last_uploaded(db=db, fcm_token=fcm_token)
                logger.info(
                    f"FCM token last uploaded more than 2 weeks ago. Re-subscribing to topic"
                )
        else:
            subscribe_topic(fcm_token)
            crud.store_fcm_token(db=db, fcm_token=fcm_token)
    except Exception as e:
        logger.error(f"Failed to handle fcm token: {e}")
