from datetime import datetime, timedelta
from io import BytesIO

from fastapi import APIRouter, Depends
from mpl_toolkits.axisartist import AxesZero
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse, StreamingResponse

from app.api.dependencies.db import get_session
from app.api.routes.devices import current_user
from app.db.repositories.measurement import MeasurementRepository
from app.db.tables.measurements import Measurements as MeasurementsTable
from app.models.user import User

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


router = APIRouter(prefix="/graphs")


async def create_graph(db: AsyncSession, device_id: str, before: datetime = None, after: datetime = None) -> BytesIO:
    repo = MeasurementRepository(MeasurementsTable, db)
    measurements = await repo.get_measurements(device_id=device_id, limit=None, after=after, before=before)
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
    "/{device_id}",
    name="device:get-measurements",
    response_class=FileResponse
)
async def requests_table(
    device_id: str,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(current_user),
):
    graph = await create_graph(db, device_id, after=datetime.now() - timedelta(days=1))
    return StreamingResponse(graph, media_type="image/png")
