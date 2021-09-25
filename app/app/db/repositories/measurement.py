from datetime import datetime
from typing import Optional, List

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

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
