import uuid

from fastapi_users import FastAPIUsers

from app.core.auth import auth_backend, get_user_manager
from app.db.tables.users import Users

fastapi_users = FastAPIUsers[Users, uuid.UUID](
    get_user_manager,
    [auth_backend],
)
