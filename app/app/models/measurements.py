from datetime import datetime
from typing import Optional

from app.models.core import IDModelMixin, CoreModel
from pydantic import Field


class MeasurementBase(CoreModel):
    """
    All common characteristics of our Measurement resource
    """

    pass


class AirMeasurement(MeasurementBase):
    co2: int = Field(..., alias="rco2")
    temperature: float = Field(..., alias="atmp")
    pm2_5: int = Field(..., alias="pm02")
    humidity: int = Field(..., alias="rhum")


class AirMeasurementCreate(AirMeasurement, MeasurementBase):
    wifi: int

    class Config:
        allow_population_by_field_name = True
        underscore_attrs_are_private = True


class AirMeasurementInDB(IDModelMixin, AirMeasurement):
    created_at: Optional[datetime]
    device_id: str


class AirMeasurementPublic(AirMeasurementInDB):
    class Config:
        allow_population_by_field_name = True
