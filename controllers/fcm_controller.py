from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy.orm import Session
from database import crud, database
from firebase.auth import verify_url_token
from firebase.firebase import subscribe_topic
from lib.auth import get_current_user
from models.user import User

router = APIRouter(
    tags=["fcm"],
    dependencies=[],
    responses={404: {"description": "Not found"}}, 
    deprecated=True
)


@router.post("/fcm", status_code=200)
async def register_fcm(token: str, current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(database.get_db)):

    try:
        existing_token = crud.find_fcm_token(db=db, fcm_token=token)

        if existing_token != None:
            logger.info(f"FCM token already registered for user {current_user.username}")

            if existing_token.lastUploadedEpoch < int(datetime.now().timestamp()) - 60*60*24*7*2:
                subscribe_topic(token)
                crud.update_fcm_token_last_uploaded(db=db, fcm_token=token)
                logger.info(f"FCM token last uploaded more than 2 weeks ago. Re-subscribing to topic")

        else:
            logger.info(f"Registering FCM token for user {current_user.username}")
            subscribe_topic(token)
            crud.store_fcm_token(db=db, fcm_token=token)

    except Exception as e:
        logger.error(f"Failed to handle fcm token: {e}")