from app.models.measurements import AirMeasurementCreate
from ward import test


@test("pydantic aliases work with payload")
def _():
    payload = '{"wifi":-57,"pm02":22,"rco2":890,"atmp":29.90,"rhum":39}'

    model = AirMeasurementCreate.parse_raw(payload)

    assert model.wifi == -57
    assert model.pm2_5 == 22
    assert model.co2 == 890
    assert model.temperature == 29.90
    assert model.humidity == 39
