from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import HTMLResponse

from app.api.dependencies.db import get_session
from app.api.dependencies.files import templates
from app.api.routes.devices import current_user
from app.db.repositories.device_request import DeviceRequestRepository
from app.db.tables.device_request import DeviceRequest as DeviceRequestTable
from app.models.user import User

router = APIRouter(prefix="/devices")


@router.get("/requests", name="device-requests:table", response_class=HTMLResponse)
async def requests_table(
    request: Request,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(current_user),
):
    request_repo = DeviceRequestRepository(DeviceRequestTable, db)
    requests = await request_repo.get_multi(sort_recent=True)
    return templates.TemplateResponse(
        "requests.html", {"request": request, "requests": requests}
    )


@router.get(
    "/requests-with-buttons",
    name="device-requests:table-with-buttons",
    response_class=HTMLResponse,
)
async def requests_table(
    request: Request,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(current_user),
):
    request_repo = DeviceRequestRepository(DeviceRequestTable, db)
    requests = await request_repo.get_multi(sort_recent=True)
    return templates.TemplateResponse(
        "requests-buttons.html", {"request": request, "requests": requests}
    )
