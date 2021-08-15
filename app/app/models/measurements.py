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
    device_id: Optional[str] = None


class AirMeasurementInDB(IDModelMixin, MeasurementBase):
    created_at: Optional[datetime]
    device_id: str
