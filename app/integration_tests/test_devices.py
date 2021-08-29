from app.db.repositories.measurement import MeasurementRepository
from app.models.measurements import AirMeasurementCreate
from fastapi import FastAPI
from httpx import AsyncClient
from integration_tests.factories import create_measurement
from integration_tests.fixtures import app, client, measurements_repo
from starlette import status
from ward import test, using


@test("a measurement is created")
@using(client=client, app=app)
async def _(app: FastAPI, client: AsyncClient):
    res = await client.post(
        app.url_path_for("device:create-measurement", device_id="test12"),
        json={"wifi": -57, "pm02": 22, "rco2": 890, "atmp": 29.90, "rhum": 39},
    )
    assert res.status_code == status.HTTP_201_CREATED


@test("bad measurements fail")
@using(client=client, app=app)
async def _(app: FastAPI, client: AsyncClient):
    res = await client.post(
        app.url_path_for("device:create-measurement", device_id="test12"),
        json={},
    )
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@test("measurements are returned")
@using(client=client, app=app, repo=measurements_repo)
async def _(app: FastAPI, client: AsyncClient, repo: MeasurementRepository):
    record = AirMeasurementCreate(
        wifi=5, co2=100, temperature=10.00, pm2_5=5, humidity=5
    )
    await create_measurement(repo, "test12", record)
    res = await client.get(
        app.url_path_for("device:get-measurements", device_id="test12"), params={}
    )
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()) == 2
