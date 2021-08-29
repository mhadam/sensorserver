import os
import warnings

import alembic
from alembic.config import Config
from app.core.config import JWT_TOKEN_PREFIX, SECRET_KEY
from app.db.repositories.measurement import MeasurementRepository
from app.db.repositories.users import UsersRepository
from app.models.user import UserCreate, UserInDB
from app.services.authentication import create_access_token_for_user
from asgi_lifespan import LifespanManager
from databases import Database
from fastapi import FastAPI
from httpx import AsyncClient
from ward import fixture, Scope


@fixture(scope=Scope.Global)
def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    os.environ["TESTING"] = "1"
    config = Config("alembic.ini")
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


@fixture(scope=Scope.Test)
def app(apply_migrations=apply_migrations) -> FastAPI:
    from app.api.server import get_application

    return get_application()


@fixture(scope=Scope.Test)
def db(app=app) -> Database:
    return app.state._db


@fixture
def measurements_repo(db=db) -> MeasurementRepository:
    return MeasurementRepository(db)


@fixture(scope=Scope.Test)
async def client(app=app) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client


@fixture
async def user(db=db) -> UserInDB:
    new_user = UserCreate(
        email="lebron@james.io", username="lebronjames", password="heatcavslakers"
    )

    user_repo = UsersRepository(db)

    existing_user = await user_repo.get_user_by_email(email=new_user.email)
    if existing_user:
        return existing_user

    return await user_repo.register_new_user(new_user)


@fixture
def authorized_client(client: AsyncClient, test_user: UserInDB) -> AsyncClient:
    access_token = create_access_token_for_user(
        user=test_user, secret_key=str(SECRET_KEY)
    )
    client.headers = {
        **client.headers,
        "Authorization": f"{JWT_TOKEN_PREFIX} {access_token}",
    }
    return client
