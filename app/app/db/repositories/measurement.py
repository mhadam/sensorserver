from app.db.repositories.base import BaseRepository
from app.db.tables.measurements import Measurements

from app.models.measurements import AirMeasurementCreate
from sqlalchemy import insert


class MeasurementRepository(BaseRepository):
    """ "
    All database actions associated with the Measurement resource
    """

    async def create_measurement(self, *, new_measurement: AirMeasurementCreate):
        query_values = new_measurement.dict(exclude={"wifi"})
        await self.db.execute(query=insert(Measurements), values=query_values)
