import contextlib
from collections import namedtuple
from datetime import datetime, timedelta
from enum import Enum, unique
from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
from fastapi import APIRouter, Depends
from mpl_toolkits.axisartist import AxesZero
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import FileResponse, StreamingResponse, HTMLResponse

from app.api.dependencies.db import get_session
from app.api.dependencies.files import templates
from app.api.routes.devices import current_user
from app.db.repositories.measurement import MeasurementRepository
from app.db.tables.measurements import Measurements as MeasurementsTable
from app.models.user import User

router = APIRouter(prefix="/graphs")


Image = namedtuple("Image", ["src", "metric"])
Device = namedtuple("Device", ["value", "text"])


@unique
class Metric(Enum):
    CO2 = "co2"
    TEMP = "temperature"
    PM2_5 = "pm2_5"
    HUMID = "humidity"


async def create_graph(
    db: AsyncSession, device_id: str, measurement_type: Metric, before: datetime = None, after: datetime = None
):
    repo = MeasurementRepository(MeasurementsTable, db)
    measurements = await repo.get_measurements(
        device_id=device_id, limit=None, after=after, before=before
    )
    fig = plt.figure()
    ax = fig.add_subplot(axes_class=AxesZero)
    data = [m.__dict__ for m in measurements]
    df = pd.DataFrame(data)
    df["temperature"] = pd.to_numeric(df["temperature"])
    df.plot(x="created_at", y=measurement_type.value)
    bio = BytesIO()
    plt.savefig(bio)
    plt.close(fig)
    bio.seek(0)
    return bio


@router.get(
    "/image/{device_id}", name="device:get-measurements"
)
async def requests_table(
    device_id: str,
    metric: Metric,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(current_user),
):
    graph = await create_graph(db, device_id, metric, after=datetime.now() - timedelta(days=1))
    return StreamingResponse(graph, media_type="image/png")


@router.get("/image", name="device:get-measurements")
async def requests_table(
    device: str,
    metric: Metric,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(current_user),
):
    graph = await create_graph(db, device, metric, after=datetime.now() - timedelta(days=1))
    return StreamingResponse(graph, media_type="image/png")


@router.get("/element", name="device:get-graphs", response_class=HTMLResponse)
async def requests_table(
    device: str,
    metric: str,
    request: Request,
    _: User = Depends(current_user),
):
    images = [Image(f"/htmx/graphs/image/{device}", metric)]
    return templates.TemplateResponse(
        "image.html", {"request": request, "images": images}
    )


@router.get("/choices", name="device:get-choices", response_class=HTMLResponse)
async def choices(
    request: Request,
    _: User = Depends(current_user),
    db: AsyncSession = Depends(get_session),
):
    repo = MeasurementRepository(MeasurementsTable, db)
    devices_ids = await repo.get_devices()
    devices = [Device(d, d) for d in devices_ids]
    return templates.TemplateResponse(
        "choices.html", {"request": request, "choices": devices}
    )
