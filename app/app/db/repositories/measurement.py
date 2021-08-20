from datetime import datetime
from typing import Optional, List

from app.db.repositories.base import BaseRepository
from app.db.tables.measurements import Measurements
from app.models.measurements import AirMeasurementCreate, AirMeasurementPublic
from sqlalchemy import insert, select, desc


class MeasurementRepository(BaseRepository):
    """ "
    All database actions associated with the Measurement resource
    """

    async def create_measurement(self, device_id: str, new_measurement: AirMeasurementCreate):
        query_values = new_measurement.dict(exclude={"wifi"})
        query_values["device_id"] = device_id
        await self.db.execute(query=insert(Measurements), values=query_values)

    async def get_measurements(
        self,
        device_id: Optional[str] = None,
        limit: int = 10,
        before: Optional[datetime] = None,
        after: Optional[datetime] = None,
    ) -> List[AirMeasurementPublic]:
        query = (
            select([Measurements])
            .where(Measurements.device_id == device_id)
            .limit(limit)
        )
        if before:
            query = query.where(Measurements.created_at < before)
        elif after:
            query = query.where(Measurements.created_at > after)
        else:
            query = query.order_by(desc(Measurements.created_at))

        rows = await self.db.fetch_all(query=query)
        return [AirMeasurementPublic(**row) for row in rows]
