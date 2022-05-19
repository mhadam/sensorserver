from datetime import datetime, timedelta
from typing import Optional

import jwt
from app.core.config import (
    SECRET_KEY,
    JWT_AUDIENCE,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    DEVICE_ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_ALGORITHM,
)
from app.models.device_auth import DeviceJWTPayload
from app.models.token import JWTMeta, JWTCreds, JWTPayload
from app.models.user import UserDB
from fastapi import HTTPException
from passlib.context import CryptContext
from pydantic import ValidationError
from starlette import status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthException(BaseException):
    """
    Custom auth exception that can be modified later on.
    """

    pass


def create_access_token_for_user(
    user: UserDB,
    secret_key: str = str(SECRET_KEY),
    audience: str = JWT_AUDIENCE,
    expires_in: int = ACCESS_TOKEN_EXPIRE_MINUTES,
) -> Optional[str]:
    if not user or not isinstance(user, UserDB):
        return None
    jwt_meta = JWTMeta(
        aud=audience,
        iat=datetime.timestamp(datetime.utcnow()),
        exp=datetime.timestamp(datetime.utcnow() + timedelta(minutes=expires_in)),
    )
    jwt_creds = JWTCreds(sub=user.email)
    token_payload = JWTPayload(
        **jwt_meta.dict(),
        **jwt_creds.dict(),
    )
    # NOTE - previous versions of pyjwt ("<2.0") returned the token as bytes insted of a string.
    # That is no longer the case and the `.decode("utf-8")` has been removed.
    access_token = jwt.encode(token_payload.dict(), secret_key, algorithm=JWT_ALGORITHM)
    return access_token


def _decode_token(token: str, secret_key: str):
    try:
        decoded_token = jwt.decode(
            token, str(secret_key), audience=JWT_AUDIENCE, algorithms=[JWT_ALGORITHM]
        )
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return decoded_token


def create_access_token_for_device(
    device_id: str,
    secret_key: str = str(SECRET_KEY),
    audience: str = JWT_AUDIENCE,
    expires_in: int = DEVICE_ACCESS_TOKEN_EXPIRE_MINUTES,
) -> Optional[str]:
    jwt_meta = JWTMeta(
        aud=audience,
        iat=datetime.timestamp(datetime.utcnow()),
        exp=datetime.timestamp(datetime.utcnow() + timedelta(minutes=expires_in)),
    )
    token_payload = DeviceJWTPayload(device_id=device_id, **jwt_meta.dict())
    # NOTE - previous versions of pyjwt ("<2.0") returned the token as bytes insted of a string.
    # That is no longer the case and the `.decode("utf-8")` has been removed.
    access_token = jwt.encode(token_payload.dict(), secret_key, algorithm=JWT_ALGORITHM)
    return access_token


def get_device_id_from_token(
    token: str, secret_key: str = str(SECRET_KEY)
) -> Optional[str]:
    decoded = _decode_token(token, secret_key)
    payload = DeviceJWTPayload(**decoded)
    return payload.device_id


def get_email_from_token(
    token: str, secret_key: str = str(SECRET_KEY)
) -> Optional[str]:
    decoded = _decode_token(token, secret_key)
    payload = JWTPayload(**decoded)
    return payload.sub
