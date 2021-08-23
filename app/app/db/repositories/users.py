from typing import Optional

from app.db.repositories.base import BaseRepository
from app.models.user import UserCreate, UserInDB
from app.db.tables.users import Users
from pydantic import EmailStr
from sqlalchemy import insert, select
from starlette import status
from starlette.exceptions import HTTPException


class UsersRepository(BaseRepository):
    async def register_new_user(self, new_user: UserCreate) -> UserInDB:
        # make sure email isn't already taken
        if await self.get_user_by_email(email=new_user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="That email is already taken. Login with that email or register with another one.",
            )
        # make sure username isn't already taken
        if await self.get_user_by_username(username=new_user.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="That username is already taken. Please try another one.",
            )
        created_user = await self.db.fetch_one(
            query=insert(Users), values={**new_user.dict(), "salt": "123"}
        )
        return UserInDB(**created_user)

    async def get_user_by_username(self, *, username: str) -> Optional[UserInDB]:
        user_record = await self.db.fetch_one(
            query=select(Users).where(Users.username == username),
        )
        if not user_record:
            return None
        return UserInDB(**user_record)

    async def get_user_by_email(self, *, email: EmailStr) -> Optional[UserInDB]:
        user_record = await self.db.fetch_one(
            query=select(Users).where(Users.email == email)
        )
        if not user_record:
            return None
        return UserInDB(**user_record)
