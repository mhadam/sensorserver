from ipaddress import IPv4Address
from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

from app.db.crud import CRUDBase
from app.db.tables.device_auth import DeviceAuth as DeviceAuthTable

from app.models.device_auth import DeviceAuthCreate, DeviceAuthUpdate, DeviceAuth


class DeviceAuthRepository(
    CRUDBase[DeviceAuthTable, DeviceAuthCreate, DeviceAuthUpdate]
):
    async def check_auth(
        self, device_id: str, ip_address: IPv4Address
    ) -> Optional[DeviceAuth]:
        try:
            model = self.model
            query = select(model).filter(
                model.device_id == device_id and model.ip_address == ip_address
            )
            result = await self.db.execute(query)
            return DeviceAuth(**result.one())
        except (NoResultFound, MultipleResultsFound):
            pass

    # async def insert_allow(
    #     db: AsyncSession, *, device_id: str, ip_address: IPv4Address
    # ) -> DeviceAuthInDb:
    #     values = {"device_id": device_id, "ip_address": ip_address}
    #
    #     query = insert(DeviceAllow).returning(*DeviceAllow.__table__.c)
    #     created = await db.execute(query=query, values=values)
    #     return DeviceAuthInDb(**created)

    # async def refresh(self):
    #     pass
    #
    # @staticmethod
    # async def get_allow(
    #     db: AsyncSession, *, device_id: str, ip_address: IPv4Address
    # ) -> DeviceAuthInDb:
    #     c = DeviceAllow.__table__.c
    #     query = select(DeviceAllow).where(
    #         c.device_id == device_id and c.ip_address == ip_address
    #     )
    #     result = await db.execute(query=query)
    #     return DeviceAuthInDb(**result)
