import ipaddress
import logging
from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Body, Depends, Response, HTTPException
from fastapi.security import OAuth2PasswordBearer
from psycopg2.errorcodes import UNIQUE_VIOLATION
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request

from app.api.dependencies.auth import fastapi_users
from app.api.dependencies.db import get_session
from app.db.repositories.device_auth import DeviceAuthRepository
from app.db.repositories.device_block import DeviceBlockRepository
from app.db.repositories.device_request import DeviceRequestRepository
from app.db.repositories.measurement import MeasurementRepository
from app.db.tables.device_auth import DeviceAuth as DeviceAuthTable
from app.db.tables.device_block import DeviceBlock as DeviceBlockTable
from app.db.tables.device_request import DeviceRequest as DeviceRequestTable
from app.db.tables.measurements import Measurements as MeasurementsTable
from app.models.device_auth import DeviceAuthCreate, DeviceAuth
from app.models.device_request import DeviceRequest
from app.models.measurements import (
    AirMeasurementCreate,
    AirMeasurementPublic,
    AirMeasurement,
    AirMeasurementCreateBody,
)
from app.models.user import User
from app.services.authentication import create_access_token_for_device, get_device_id_from_token

logger = logging.getLogger(__name__)

router = APIRouter()

current_user = fastapi_users.current_user(active=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post(
    "/devices/{device_id}:measure",
    name="device:create-measurement",
    status_code=status.HTTP_201_CREATED,
)
async def create_new_measurement(
    device_id: str,
    request: Request,
    new_measurement: AirMeasurementCreateBody = Body(...),
    db: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    token_device_id = get_device_id_from_token(token)
    if token_device_id != device_id:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

    auth_repo = DeviceAuthRepository(DeviceAuthTable, db)
    ip_address = request.client.host
    maybe_auth = await auth_repo.check_auth(device_id, ip_address)
    if maybe_auth is None:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

    repo = MeasurementRepository(MeasurementsTable, db)
    obj = AirMeasurementCreate(device_id=device_id, **new_measurement.dict())
    await repo.create(obj)


@router.get(
    "/devices/{device_id}/measurements",
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


def get_ip_address(request: Request) -> ipaddress.IPv4Address:
    return ipaddress.IPv4Address(request.headers.get('x-forwarded-host', request.client.host))


@router.get(
    "/devices/{device_id}:knock",
    name="device:knock",
    status_code=status.HTTP_200_OK,
)
async def device_knock(
    device_id: str,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_session),
):
    """Knock for authorization, repeatedly call until allowed to report.
    Response will have a JWT token as a header.
    """
    auth_repo = DeviceAuthRepository(DeviceAuthTable, db)
    request_repo = DeviceRequestRepository(DeviceRequestTable, db)
    ip_address = get_ip_address(request)
    maybe_auth = await auth_repo.check_auth(device_id, ip_address)
    logger.info(maybe_auth)
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
    "/requests/{request_id}:approve",
    name="requests:approve",
    status_code=status.HTTP_200_OK,
)
async def approve_request(
    request_id: int,
    db: AsyncSession = Depends(get_session),
    user: User = Depends(current_user),
):
    request_repo = DeviceRequestRepository(DeviceRequestTable, db)
    maybe_request = await request_repo.get(request_id)
    if maybe_request is not None:
        auth_repo = DeviceAuthRepository(DeviceAuthTable, db)
        obj_in = DeviceAuthCreate(
            device_id=maybe_request.device_id, ip_address=maybe_request.ip_address, user_id=user.id
        )
        try:
            await auth_repo.create(obj_in)
        except IntegrityError as e:
            try:
                if e.orig.pgcode == UNIQUE_VIOLATION:
                    return Response(status_code=status.HTTP_400_BAD_REQUEST)
            except AttributeError:
                pass
            raise e
        await request_repo.remove(request_id)
        return Response(status_code=status.HTTP_200_OK)
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.get(
    "/requests/{request_id}:block",
    name="requests:block",
    status_code=status.HTTP_200_OK,
)
async def block_request(
    request_id: int,
    db: AsyncSession = Depends(get_session),
    user: User = Depends(current_user),
):
    request_repo = DeviceRequestRepository(DeviceRequestTable, db)
    maybe_request = await request_repo.get(request_id)
    if maybe_request is not None:
        block_repo = DeviceBlockRepository(DeviceBlockTable, db)
        obj_in = DeviceBlockTable(
            device_id=maybe_request.device_id, ip_address=maybe_request.ip_address
        )
        try:
            await block_repo.create(obj_in)
        except IntegrityError as e:
            try:
                if e.orig.pgcode == UNIQUE_VIOLATION:
                    return Response(status_code=status.HTTP_400_BAD_REQUEST)
            except AttributeError:
                pass
            raise e
        await request_repo.remove(request_id)
        return Response(status_code=status.HTTP_200_OK)
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.get(
    "/requests",
    name="requests:get-all",
    status_code=status.HTTP_200_OK,
)
async def get_requests(
    db: AsyncSession = Depends(get_session),
    user: User = Depends(current_user),
) -> List[DeviceRequest]:
    request_repo = DeviceRequestRepository(DeviceRequestTable, db)
    result = await request_repo.get_multi(sort_recent=True)
    return [DeviceRequest.from_orm(r) for r in result]


@router.get(
    "/devices",
    name="device:get-all-auths",
    status_code=status.HTTP_200_OK,
)
async def get_approvals(
    db: AsyncSession = Depends(get_session),
    _: User = Depends(current_user),
) -> List[DeviceAuth]:
    auth_repo = DeviceAuthRepository(DeviceAuthTable, db)
    results = await auth_repo.get_multi(sort_recent=True)
    logger.info(results)
    return [DeviceAuth.from_orm(r[0]) for r in results]
