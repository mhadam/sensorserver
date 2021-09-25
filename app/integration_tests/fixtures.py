import warnings

from alembic.command import upgrade, downgrade
from alembic.config import Config
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from fastapi_users.db import SQLAlchemyUserDatabase
from httpx import AsyncClient
from ward import fixture, Scope

from app.core.config import JWT_TOKEN_PREFIX, SECRET_KEY
from app.db.repositories.measurement import MeasurementRepository
from app.db.tables.users import Users
from app.models.user import UserCreate, UserDB


@fixture(scope=Scope.Global)
def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    config = Config("alembic.ini")
    upgrade(config, "head")
    yield
    downgrade(config, "base")


@fixture(scope=Scope.Test)
def app(apply_migrations=apply_migrations) -> FastAPI:
    from app.api.server import get_application

    return get_application()


# @fixture(scope=Scope.Test)
# def db(app=app) -> Database:
#     return app.state._db


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
async def user(db=db) -> UserDB:
    user_table = Users.__table__
    user_db = SQLAlchemyUserDatabase(UserDB, db, user_table)
    new_user = UserCreate(
        email="lebron@james.io", username="lebronjames", password="heatcavslakers"
    )

    existing_user = await user_db.get_user_by_email(email=new_user.email)
    if existing_user:
        return existing_user

    return await user_db.register_new_user(new_user)


@fixture
def authorized_client(client: AsyncClient, test_user: UserDB) -> AsyncClient:
    # access_token = create_access_token(user=test_user, secret_key=str(SECRET_KEY))
    # client.headers = {
    #     **client.headers,
    #     "Authorization": f"{JWT_TOKEN_PREFIX} {access_token}",
    # }
    return client
