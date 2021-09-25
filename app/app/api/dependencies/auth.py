from app.core.auth import auth_backends
from app.db.database import database
from app.db.tables.users import Users

from app.models.user import UserDB, User, UserCreate, UserUpdate
from fastapi_users import FastAPIUsers
from fastapi_users.db import SQLAlchemyUserDatabase

user_table = Users.__table__
user_db = SQLAlchemyUserDatabase(UserDB, database, user_table)

fastapi_users = FastAPIUsers(
    user_db, auth_backends, User, UserCreate, UserUpdate, UserDB
)
