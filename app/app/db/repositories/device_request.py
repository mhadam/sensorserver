from ipaddress import IPv6Address, IPv4Address
from typing import Optional, Union

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
        self, device_id: str, ip_address: Union[IPv4Address, IPv6Address]
    ) -> Optional[DeviceRequest]:
        try:
            model = self.model
            new_request = model(device_id=device_id, ip_address=str(ip_address))
            self.db.add(new_request)
            await self.db.commit()
            await self.db.refresh(new_request)
            return DeviceRequest.from_orm(new_request)
        except (NoResultFound, MultipleResultsFound, IntegrityError):
            pass

    async def get_device(self, device_id: str) -> Optional[DeviceRequest]:
        model = self.model
        query = select(model).filter(model.device_id == device_id)
        result = await self.db.execute(query)
        return DeviceRequest.from_orm(result.scalars().first())

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
