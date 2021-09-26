from typing import Optional

from pydantic import IPvAnyAddress
from sqlalchemy import select, delete
from sqlalchemy.exc import NoResultFound, MultipleResultsFound, IntegrityError

from app.db.crud import CRUDBase
from app.db.tables.device_request import DeviceRequest as DeviceRequestTable
from app.models.device_request import (
    DeviceRequest,
    DeviceRequestCreate,
    DeviceRequestUpdate,
)


class DeviceRequestRepository(
    CRUDBase[DeviceRequestTable, DeviceRequestCreate, DeviceRequestUpdate]
):
    async def add_only_new(
        self, device_id: str, ip_address: IPvAnyAddress
    ) -> Optional[DeviceRequest]:
        try:
            model = self.model
            new_request = model(device_id=device_id, ip_address=ip_address)
            self.db.add(new_request)
            return DeviceRequest.from_orm(new_request)
        except (NoResultFound, MultipleResultsFound, IntegrityError):
            pass

    async def check_request(
        self, device_id: str, ip_address: IPvAnyAddress
    ) -> Optional[DeviceRequest]:
        try:
            model = self.model
            query = select(model).filter(
                model.device_id == device_id and model.ip_address == ip_address
            )
            result = await self.db.execute(query)
            return DeviceRequest.from_orm(result.scalars().one())
        except (MultipleResultsFound, NoResultFound):
            return

    async def remove_request(self, device_id: str, ip_address: IPvAnyAddress):
        model = self.model
        statement = delete(model).where(
            model.device_id == device_id and model.ip_address == ip_address
        )
        await self.db.execute(statement)
