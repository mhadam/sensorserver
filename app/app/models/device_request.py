from pydantic import IPvAnyAddress

from app.models.core import CoreModel, IDModelMixin, DateTimeModelMixin


class DeviceRequest(CoreModel, IDModelMixin, DateTimeModelMixin):
    device_id: str
    ip_address: IPvAnyAddress


class DeviceRequestCreate(CoreModel):
    device_id: str
    ip_address: IPvAnyAddress


class DeviceRequestUpdate(CoreModel):
    device_id: str
    ip_address: IPvAnyAddress
