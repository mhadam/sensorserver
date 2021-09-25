from fastapi_users.db.sqlalchemy import GUID
from sqlalchemy import Column, BigInteger, Table, Text, ForeignKey, UniqueConstraint

from app.db.tables import Base, timestamps


class DeviceAuth(Base):
    __tablename__ = "device_auth"

    __table__ = Table(
        "device_auth",
        Base.metadata,
        Column("id", BigInteger, primary_key=True),
        Column("device_id", Text, nullable=False, index=True),
        Column(
            "user_id",
            GUID,
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        Column("ip_address", Text, nullable=False),
        UniqueConstraint("device_id", "ip_address"),
        *timestamps()
    )
