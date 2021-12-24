from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import HTMLResponse

from app.api.dependencies.db import get_session
from app.api.routes.devices import current_user
from app.api.server import templates
from app.db.repositories.device_request import DeviceRequestRepository
from app.db.tables.device_request import DeviceRequest as DeviceRequestTable
from app.models.user import User

router = APIRouter()


@router.get(
    "/requests",
    name="requests:list",
    response_class=HTMLResponse
)
async def create_new_measurement(
    db: AsyncSession = Depends(get_session),
    _: User = Depends(current_user),
):
    request_repo = DeviceRequestRepository(DeviceRequestTable, db)
    request_repo.get_multi()
    return templates.TemplateResponse("requests.html", {

    })
