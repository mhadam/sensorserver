from ipaddress import IPv4Address

from app.db.repositories.base import BaseRepository
from app.db.tables.device_allow import DeviceAllow
from app.models.device_allow import DeviceAuthInDb
from sqlalchemy import insert, select


class DeviceAuthRepository(BaseRepository):
    async def insert_allow(
        self, device_id: str, ip_address: IPv4Address
    ) -> DeviceAuthInDb:
        values = {"device_id": device_id, "ip_address": ip_address}
        query = insert(DeviceAllow).returning(*DeviceAllow.__table__.c)
        created = await self.db.execute(query=query, values=values)
        return DeviceAuthInDb(**created)

    async def refresh(self):
        pass

    async def find_allow(
        self, device_id: str, ip_address: IPv4Address
    ) -> DeviceAuthInDb:
        c = DeviceAllow.__table__.c
        query = select(DeviceAllow).where(
            c.device_id == device_id and c.ip_address == ip_address
        )
        result = await self.db.execute(query=query)
        return DeviceAuthInDb(**result)
