from typing import Optional

from pydantic import IPvAnyAddress
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
    async def add_only_new(self, device_id: str, ip_address: IPvAnyAddress):
        try:
            model = self.model
            self.db.add(model(device_id=device_id, ip_address=ip_address))
            await self.db.commit()
            return DeviceRequest(device_id=device_id, ip_address=ip_address)
        except (NoResultFound, MultipleResultsFound, IntegrityError):
            pass

    async def check_request(
        self, device_id: str, ip_address: IPvAnyAddress
    ) -> Optional[DeviceRequest]:
        try:
            model = self.model
            result = (
                await self.db.query(self.model)
                .filter(model.device_id == device_id and model.ip_address == ip_address)
                .first()
            )
            return DeviceRequest(**result)
        except (NoResultFound, MultipleResultsFound):
            pass

    async def remove_request(self, device_id: str, ip_address: IPvAnyAddress):
        try:
            model = self.model
            statement = model.delete().where(model.device_id == device_id and model.ip_address == ip_address)
            await self.db.execute(statement)
        except (NoResultFound, MultipleResultsFound):
            pass
