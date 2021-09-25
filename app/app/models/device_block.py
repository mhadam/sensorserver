from pydantic import IPvAnyAddress

from app.models.core import CoreModel, IDModelMixin, DateTimeModelMixin


class DeviceBlock(CoreModel, IDModelMixin, DateTimeModelMixin):
    device_id: str
    ip_address: IPvAnyAddress


class DeviceBlockCreate(CoreModel):
    device_id: str
    ip_address: IPvAnyAddress


class DeviceBlockUpdate(CoreModel):
    device_id: str
    ip_address: IPvAnyAddress


class DeviceBlockDelete(CoreModel):
    device_id: str
    ip_address: IPvAnyAddress
