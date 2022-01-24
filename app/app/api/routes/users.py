from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import Response

from app.api.dependencies.auth import fastapi_users
from app.api.dependencies.db import get_session
from app.core.auth import auth_backend
from app.models.user import User

current_user = fastapi_users.current_user(active=True)

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=True),
    prefix="/auth/cookie",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_users_router(),
    prefix="/users",
    tags=["users"],
)
