import logging

from app.db.repositories.measurement import MeasurementRepository
from app.dependencies.database import get_repository
from app.models.measurements import AirMeasurementCreate
from fastapi import APIRouter, Body, Depends
from starlette.status import HTTP_201_CREATED

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/device/{device_id}:measure",
    name="measurements:create-measurement",
    status_code=HTTP_201_CREATED,
)
async def create_new_measurement(
    device_id: str,
    new_measurement: AirMeasurementCreate = Body(...),
    measurement_repo: MeasurementRepository = Depends(
        get_repository(MeasurementRepository)
    ),
):
    await measurement_repo.create_measurement(
        new_measurement=new_measurement.copy(update={"device_id": device_id})
    )
