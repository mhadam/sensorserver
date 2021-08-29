from typing import Optional

from app.db.repositories.base import BaseRepository
from app.db.tables.users import Users
from app.models.user import UserCreate, UserInDB
from app.services.authentication import hash_with_salt, verify_password
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
        user_password = hash_with_salt(new_user.password)
        hashed_new_user = new_user.copy(update=user_password.dict())
        created_user = await self.db.fetch_one(
            query=insert(Users).returning(*Users.__table__.c),
            values={**hashed_new_user.dict()},
        )
        return UserInDB(**created_user)

    async def get_user_by_username(self, *, username: str) -> Optional[UserInDB]:
        user_record = await self.db.fetch_one(
            query=select([Users]).where(Users.username == username),
        )
        if not user_record:
            return None
        return UserInDB(**user_record)

    async def get_user_by_email(self, *, email: EmailStr) -> Optional[UserInDB]:
        user_record = await self.db.fetch_one(
            query=select([Users]).where(Users.email == email)
        )
        if not user_record:
            return None
        return UserInDB(**user_record)

    async def authenticate_user(
        self, *, email: EmailStr, password: str
    ) -> Optional[UserInDB]:
        # make user user exists in db
        user = await self.get_user_by_email(email=email)
        if not user:
            return None
        # if submitted password doesn't match
        if not verify_password(
            password=password, salt=user.salt, hashed_pw=user.password
        ):
            return None
        return user
