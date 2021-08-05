from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import HTTP_404_NOT_FOUND
from ward import test


@test("test route exists")
async def _(app: FastAPI, client: AsyncClient):
    res = await client.post(
        app.url_path_for("measurements:create-measurement"), json={}
    )
    assert res.status_code != HTTP_404_NOT_FOUND
