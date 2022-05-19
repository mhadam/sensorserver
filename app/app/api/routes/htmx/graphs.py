from collections import namedtuple
from datetime import datetime, timedelta
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


Image = namedtuple("Image", ["src"])
Device = namedtuple("Device", ["value", "text"])


async def create_graph(
    db: AsyncSession, device_id: str, before: datetime = None, after: datetime = None
) -> BytesIO:
    repo = MeasurementRepository(MeasurementsTable, db)
    measurements = await repo.get_measurements(
        device_id=device_id, limit=None, after=after, before=before
    )
    fig = plt.figure()
    ax = fig.add_subplot(axes_class=AxesZero)
    data = [m.__dict__ for m in measurements if m.co2 > 0]
    df = pd.DataFrame(data)
    df.plot(x="created_at", y="co2")
    bio = BytesIO()
    plt.savefig(bio)
    bio.seek(0)
    return bio


@router.get(
    "/image/{device_id}", name="device:get-measurements", response_class=FileResponse
)
async def requests_table(
    device_id: str,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(current_user),
):
    graph = await create_graph(db, device_id, after=datetime.now() - timedelta(days=1))
    return StreamingResponse(graph, media_type="image/png")


@router.get("/image", name="device:get-measurements", response_class=FileResponse)
async def requests_table(
    device: str,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(current_user),
):
    graph = await create_graph(db, device, after=datetime.now() - timedelta(days=1))
    return StreamingResponse(graph, media_type="image/png")


@router.get("/element", name="device:get-graphs", response_class=HTMLResponse)
async def requests_table(
    device: str,
    request: Request,
    _: User = Depends(current_user),
):
    images = [Image(f"/htmx/graphs/image/{device}")]
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
