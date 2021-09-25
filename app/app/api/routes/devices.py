import logging
from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Body, Depends, Response, HTTPException
from pydantic import IPvAnyAddress
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request

from app.api.dependencies.auth import fastapi_users
from app.api.dependencies.db import get_session
from app.db.repositories.device_auth import DeviceAuthRepository
from app.db.repositories.device_request import DeviceRequestRepository
from app.db.repositories.measurement import MeasurementRepository
from app.db.tables.device_auth import DeviceAuth as DeviceAuthTable, DeviceAuth
from app.db.tables.device_request import DeviceRequest as DeviceRequestTable
from app.models.device_auth import DeviceAuthCreate
from app.models.measurements import (
    AirMeasurementCreate,
    AirMeasurementPublic,
    AirMeasurement,
    AirMeasurementCreateBody,
)
from app.models.user import User
from app.services.authentication import create_access_token_for_device

logger = logging.getLogger(__name__)

router = APIRouter()

current_user = fastapi_users.current_user(active=True)


@router.post(
    "/device/{device_id}:measure",
    name="device:create-measurement",
    status_code=status.HTTP_201_CREATED,
)
async def create_new_measurement(
    device_id: str,
    request: Request,
    new_measurement: AirMeasurementCreateBody = Body(...),
    db: AsyncSession = Depends(get_session),
):
    auth_repo = DeviceAuthRepository(DeviceAuthTable, db)
    ip_address = IPvAnyAddress(request.client.host)
    maybe_auth = await auth_repo.check_auth(device_id, ip_address)
    if maybe_auth is not None:
        repo = MeasurementRepository(AirMeasurement, db)
        obj = AirMeasurementCreate(device_id=device_id, **new_measurement.dict())
        return repo.create(obj)
    return Response(status_code=status.HTTP_401_UNAUTHORIZED)


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
    db: AsyncSession = Depends(get_session),
    limit: int = 10,
    before: Optional[datetime] = None,
    after: Optional[datetime] = None,
) -> List[AirMeasurementPublic]:
    repo = MeasurementRepository(AirMeasurement, db)
    return await repo.get_measurements(
        device_id=device_id, limit=limit, before=before, after=after
    )


@router.get(
    "/device/{device_id}:knock",
    name="device:knock",
    status_code=status.HTTP_200_OK,
)
async def authorize_device(
    device_id: str,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_session),
):
    auth_repo = DeviceAuthRepository(DeviceAuthTable, db)
    request_repo = DeviceRequestRepository(DeviceRequestTable, db)
    ip_address = IPvAnyAddress(request.client.host)
    maybe_auth = auth_repo.check_auth(device_id, ip_address)
    if maybe_auth is None:
        await request_repo.add_only_new(device_id, ip_address)
        return Response(status_code=status.HTTP_201_CREATED)

    jwt = create_access_token_for_device(device_id)
    if jwt is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="jwt is empty"
        )
    response.headers["Authorization"] = "Bearer " + jwt


@router.get(
    "/request/{device_id}:approve",
    name="request:approve",
    status_code=status.HTTP_200_OK,
)
async def approve_request(
    device_id: str,
    request: Request,
    db: AsyncSession = Depends(get_session),
    user: User = Depends(current_user),
):
    request_repo = DeviceRequestRepository(DeviceRequestTable, db)
    ip_address = IPvAnyAddress(request.client.host)
    if request_repo.check_request(device_id, ip_address):
        auth_repo = DeviceAuthRepository(DeviceAuthTable, db)
        obj_in = DeviceAuthCreate(device_id=device_id, ip_address=ip_address, user=user.id)
        await auth_repo.create(obj_in)
        await request_repo.remove_request(device_id, ip_address)
    return Response(status_code=status.HTTP_404_NOT_FOUND)
