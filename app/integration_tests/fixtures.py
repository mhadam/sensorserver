import os
import warnings

import alembic
from alembic.config import Config
from app.db.repositories.measurement import MeasurementRepository
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
