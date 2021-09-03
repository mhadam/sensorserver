from ipaddress import IPv4Address

from app.models.core import DateTimeModelMixin, IDModelMixin
from app.models.token import JWTMeta


class DeviceJWTPayload(JWTMeta):
    """
    JWT Payload right before it's encoded - combine meta and username
    """

    device_id: str


class DeviceAuthInDb(IDModelMixin, DateTimeModelMixin):
    device_id: str
    user_id: int
    ip_address: IPv4Address
