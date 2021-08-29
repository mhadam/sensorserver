from app.db.tables import Base, timestamps
from sqlalchemy import Column, BigInteger, Table, Text, ForeignKey
from sqlalchemy.orm import relationship


class DeviceAllow(Base):
    __tablename__ = "device_allow"

    __table__ = Table(
        "device_allow",
        Base.metadata,
        Column("id", BigInteger, primary_key=True),
        Column("device_id", Text, nullable=False, index=True),
        Column(
            "user_id",
            BigInteger,
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        Column("ip_address", Text, nullable=False),
        Column("refresh_token", Text, nullable=True),
        relationship("Users", back_populates="device_auths"),
        *timestamps()
    )
