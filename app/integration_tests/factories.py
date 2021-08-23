from app.db.repositories.measurement import MeasurementRepository
from app.models.measurements import AirMeasurementCreate
from ward import fixture


@fixture
def new_create_measurement() -> AirMeasurementCreate:
    return AirMeasurementCreate(
        wifi="5",
        _device_id="test12",
        co2=5,
        temperature=35.00,
        pm2_5=5,
        humidity=5,
    )


async def create_measurement(
    repo: MeasurementRepository, device_id: str, record: AirMeasurementCreate
):
    await repo.create_measurement(device_id, new_measurement=record)
