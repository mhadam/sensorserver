from datetime import datetime, timedelta
from typing import Optional

import bcrypt
import jwt
from app.core.config import (
    SECRET_KEY,
    JWT_AUDIENCE,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_ALGORITHM,
)
from app.models.token import JWTMeta, JWTCreds, JWTPayload
from fastapi import HTTPException
from passlib.context import CryptContext

from app.models.user import UserPasswordUpdate, UserInDB
from pydantic import ValidationError
from starlette import status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthException(BaseException):
    """
    Custom auth exception that can be modified later on.
    """

    pass


def verify_password(password: str, salt: str, hashed_pw: str) -> bool:
    return pwd_context.verify(password + salt, hashed_pw)


def hash_with_salt(plaintext_password: str) -> UserPasswordUpdate:
    salt = bcrypt.gensalt().decode()
    hashed_password = pwd_context.hash(plaintext_password + salt)
    return UserPasswordUpdate(salt=salt, password=hashed_password)


def create_access_token_for_user(
    user: UserInDB,
    secret_key: str = str(SECRET_KEY),
    audience: str = JWT_AUDIENCE,
    expires_in: int = ACCESS_TOKEN_EXPIRE_MINUTES,
) -> Optional[str]:
    if not user or not isinstance(user, UserInDB):
        return None
    jwt_meta = JWTMeta(
        aud=audience,
        iat=datetime.timestamp(datetime.utcnow()),
        exp=datetime.timestamp(datetime.utcnow() + timedelta(minutes=expires_in)),
    )
    jwt_creds = JWTCreds(sub=user.email, username=user.username)
    token_payload = JWTPayload(
        **jwt_meta.dict(),
        **jwt_creds.dict(),
    )
    # NOTE - previous versions of pyjwt ("<2.0") returned the token as bytes insted of a string.
    # That is no longer the case and the `.decode("utf-8")` has been removed.
    access_token = jwt.encode(token_payload.dict(), secret_key, algorithm=JWT_ALGORITHM)
    return access_token


def get_username_from_token(token: str, secret_key: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(
            token, str(secret_key), audience=JWT_AUDIENCE, algorithms=[JWT_ALGORITHM]
        )
        payload = JWTPayload(**decoded_token)
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload.username
