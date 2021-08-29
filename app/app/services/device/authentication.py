from datetime import datetime, timedelta
from typing import Optional

import jwt
from app.core.config import (
    SECRET_KEY,
    JWT_AUDIENCE,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_ALGORITHM,
)
from app.models.device_allow import DeviceJWTCreds, DeviceJWTPayload
from app.models.token import JWTMeta
from fastapi import HTTPException
from pydantic import ValidationError
from starlette import status


def create_access_token_for_device(
    device_id: str,
    secret_key: str = str(SECRET_KEY),
    audience: str = JWT_AUDIENCE,
    expires_in: int = ACCESS_TOKEN_EXPIRE_MINUTES,
) -> Optional[str]:
    if not device_id:
        return None
    jwt_meta = JWTMeta(
        aud=audience,
        iat=datetime.timestamp(datetime.utcnow()),
        exp=datetime.timestamp(datetime.utcnow() + timedelta(minutes=expires_in)),
    )
    jwt_creds = DeviceJWTCreds(device_id=device_id)
    token_payload = DeviceJWTPayload(
        **jwt_meta.dict(),
        **jwt_creds.dict(),
    )
    # NOTE - previous versions of pyjwt ("<2.0") returned the token as bytes insted of a string.
    # That is no longer the case and the `.decode("utf-8")` has been removed.
    access_token = jwt.encode(token_payload.dict(), secret_key, algorithm=JWT_ALGORITHM)
    return access_token


def get_device_id_from_token(
    token: str, secret_key: str = str(SECRET_KEY)
) -> Optional[str]:
    try:
        decoded_token = jwt.decode(
            token, str(secret_key), audience=JWT_AUDIENCE, algorithms=[JWT_ALGORITHM]
        )
        payload = DeviceJWTPayload(**decoded_token)
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload.device_id
