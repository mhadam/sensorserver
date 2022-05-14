from datetime import datetime
from typing import Optional, List

from sqlalchemy import select, desc

from app.db.crud import CRDBase
from app.db.tables.measurements import Measurements
from app.models.measurements import (
    AirMeasurement,
    AirMeasurementCreate,
    AirMeasurementPublic,
)


class MeasurementRepository(CRDBase[AirMeasurement, AirMeasurementCreate]):
    """ "
    All database actions associated with the Measurement resource
    """

    async def get_devices(self) -> List[str]:
        query = select([Measurements.device_id]).distinct()
        result = await self.db.execute(statement=query)
        return result.scalars().all()

    async def get_measurements(
        self,
        device_id: Optional[str] = None,
        limit: Optional[int] = 10,
        before: Optional[datetime] = None,
        after: Optional[datetime] = None,
    ) -> List[AirMeasurementPublic]:
        query = (
            select([Measurements])
            .where(Measurements.device_id == device_id)
            .limit(limit)
            .order_by(desc(Measurements.created_at))
        )
        if before:
            query = query.where(Measurements.created_at < before)
        if after:
            query = query.where(Measurements.created_at > after)

        result = await self.db.execute(statement=query)
        return result.scalars().all()
