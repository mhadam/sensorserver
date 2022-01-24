from ipaddress import IPv4Address
from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import MultipleResultsFound

from app.db.crud import CRUDBase
from app.models.device_block import DeviceBlock, DeviceBlockCreate, DeviceBlockUpdate


class DeviceBlockRepository(
    CRUDBase[DeviceBlock, DeviceBlockCreate, DeviceBlockUpdate]
):
    async def check_block(
        self, device_id: str, ip_address: IPv4Address
    ) -> Optional[DeviceBlock]:
        try:
            model = self.model
            query = select(model).filter(
                model.device_id == device_id and model.ip_address == str(ip_address)
            )
            result = await self.db.execute(query)
            return result.one_or_none()
        except MultipleResultsFound:
            pass
