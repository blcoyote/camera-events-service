from typing import Annotated
from fastapi import Depends, HTTPException, Header
from fastapi.security import HTTPBearer
from firebase_admin import app_check
from firebase_admin import auth
import jwt
from loguru import logger

bearer_scheme = HTTPBearer(auto_error=False)


def verify_user_check(X_token: Annotated[str, Header()] = "") -> None:
    if not X_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        auth_check_claims = auth.verify_id_token(X_token)
        logger.info(f"successfilly vallidated token for: {auth_check_claims['email']}")
        # If verify_token() succeeds, okay to continue to route handler.
    except (ValueError, jwt.exceptions.DecodeError):
        # Token is invalid, forbidden
        raise HTTPException(status_code=403, detail="Invalid token")
    except Exception as e:
        # Token is invalid, forbidden
        logger.error(f"AppCheckError: {e}")
        raise HTTPException(status_code=403, detail="Invalid token")
