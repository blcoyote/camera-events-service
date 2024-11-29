from typing import Annotated
from fastapi import HTTPException, Header, Query
from fastapi.security import HTTPBearer
from firebase_admin import auth
import jwt
from loguru import logger

bearer_scheme = HTTPBearer(auto_error=False)


def verify_token(token: str) -> dict:
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        auth_check_claims = auth.verify_id_token(token)
        logger.info(f"successfully validated token for: {auth_check_claims['email']}")
        # If verify_token() succeeds, okay to continue to route handler.
    except (ValueError, jwt.exceptions.DecodeError):
        # Token is invalid, forbidden
        raise HTTPException(status_code=403, detail="Invalid token")
    except Exception as e:
        # Token is invalid, forbidden
        logger.error(f"AppCheckError: {e}")
        raise HTTPException(status_code=403, detail="Invalid token")


def verify_user_check(X_token: Annotated[str, Header()] = "") -> None:
    verify_token(X_token)


def verify_url_token(token: Annotated[str | None, Query()]) -> None:
    verify_token(token)
