from datetime import datetime
from typing import Optional, List

from sqlalchemy import select, desc
from sqlalchemy.orm import Session

from app.db.crud import CRDBase
from app.db.tables.measurements import Measurements
from app.models.measurements import AirMeasurementCreate, AirMeasurementPublic, AirMeasurement


class MeasurementRepository(CRDBase[AirMeasurement, AirMeasurementCreate]):
    """ "
    All database actions associated with the Measurement resource
    """

    async def create(self, db: Session, *, device_id: str, new_measurement: AirMeasurementCreate) -> AirMeasurement:
        query_values = new_measurement.dict(exclude={"wifi"})
        query_values["device_id"] = device_id
        super().create(db, obj_in=query_values)
        # await self.db.execute(query=insert(Measurements), values=query_values)

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
