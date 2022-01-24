from fastapi_users import FastAPIUsers

from app.core.auth import auth_backend, get_user_manager
from app.models.user import UserDB, User, UserCreate, UserUpdate

fastapi_users = FastAPIUsers(
    get_user_manager, [auth_backend], User, UserCreate, UserUpdate, UserDB
)
