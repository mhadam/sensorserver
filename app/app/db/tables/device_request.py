from sqlalchemy import Column, BigInteger, Table, Text, UniqueConstraint

from app.db.tables import Base, timestamps


class DeviceRequest(Base):
    __tablename__ = "device_request"

    __table__ = Table(
        "device_request",
        Base.metadata,
        Column("id", BigInteger, primary_key=True),
        Column("device_id", Text, nullable=False, index=True),
        Column("ip_address", Text, nullable=False),
        *timestamps(),
        UniqueConstraint("device_id", "ip_address")
    )
