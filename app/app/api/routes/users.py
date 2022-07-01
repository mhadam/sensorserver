from fastapi import APIRouter

from app.api.dependencies.auth import fastapi_users
from app.core.auth import auth_backend
from app.models.user import UserRead, UserUpdate

current_user = fastapi_users.current_user(active=True)

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=True),
    prefix="/auth/cookie",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
