from ipaddress import IPv4Address
from typing import Optional

from pydantic import UUID4

from app.models.core import IDModelMixin, DateTimeModelMixin, CoreModel
from app.models.token import JWTMeta


class DeviceJWTPayload(JWTMeta):
    """
    JWT Payload right before it's encoded - combine meta and username
    """

    device_id: str


class DeviceAuth(CoreModel, IDModelMixin, DateTimeModelMixin):
    device_id: str
    ip_address: IPv4Address
    user_id: Optional[UUID4]

    class Config:
        orm_mode = True


class DeviceAuthUpdate(CoreModel):
    device_id: str
    ip_address: IPv4Address
    user_id: Optional[UUID4] = None


class DeviceAuthCreate(CoreModel):
    device_id: str
    ip_address: IPv4Address
    user_id: UUID4


class DeviceAuthApproval(CoreModel):
    user_id: UUID4
