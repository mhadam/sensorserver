from collections import namedtuple

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response

from app.api.dependencies.db import get_session
from app.api.dependencies.files import templates
from app.api.routes.users import current_user
from app.db.repositories.measurement import MeasurementRepository
from app.db.tables.measurements import Measurements as MeasurementsTable
from app.models.user import User

router = APIRouter(prefix="/current")


Device = namedtuple("Device", ["value", "text"])


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
        "current-choices.html", {"request": request, "choices": devices}
    )


@router.get("/reading", name="device:reading", response_class=HTMLResponse)
async def reading(
    device: str,
    request: Request,
    _: User = Depends(current_user),
    db: AsyncSession = Depends(get_session),
):
    repo = MeasurementRepository(MeasurementsTable, db)
    measurement = await repo.get_measurements(device_id=device, limit=1)
    if len(measurement) != 1:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return templates.TemplateResponse(
        "reading.html", {"request": request, "reading": measurement[0]}
    )