from datetime import datetime
import logging
from typing import Optional, List

from app.db.repositories.measurement import MeasurementRepository
from app.dependencies.database import get_repository
from app.models.measurements import AirMeasurementCreate, AirMeasurementPublic
from fastapi import APIRouter, Body, Depends
from starlette import status

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/device/{device_id}:measure",
    name="device:create-measurement",
    status_code=status.HTTP_201_CREATED,
)
async def create_new_measurement(
    device_id: str,
    new_measurement: AirMeasurementCreate = Body(...),
    measurement_repo: MeasurementRepository = Depends(
        get_repository(MeasurementRepository)
    ),
):
    await measurement_repo.create_measurement(device_id, new_measurement)


@router.get(
    "/device/{device_id}/measurements",
    name="device:get-measurements",
    status_code=status.HTTP_200_OK,
    response_model=List[AirMeasurementPublic],
    response_model_by_alias=False,
    response_model_exclude_unset=True,
)
async def get_device_measurements(
    device_id: str,
    measurement_repo: MeasurementRepository = Depends(
        get_repository(MeasurementRepository)
    ),
    limit: int = 10,
    before: Optional[datetime] = None,
    after: Optional[datetime] = None,
) -> List[AirMeasurementPublic]:
    return await measurement_repo.get_measurements(
        device_id=device_id, limit=limit, before=before, after=after
    )
