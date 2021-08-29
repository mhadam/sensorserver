from ipaddress import IPv4Address
from typing import Optional

from app.models.core import CoreModel, DateTimeModelMixin, IDModelMixin
from app.models.token import JWTMeta
from pydantic import BaseModel


class DeviceJWTCreds(CoreModel):
    """How we'll identify devices"""

    device_id: str


class DeviceJWTPayload(JWTMeta, DeviceJWTCreds):
    """
    JWT Payload right before it's encoded - combine meta and username
    """

    pass


class DeviceAuthInDb(BaseModel, IDModelMixin, DateTimeModelMixin):
    device_id: str
    user_id: int
    ip_address: IPv4Address
    refresh_token: Optional[str]
