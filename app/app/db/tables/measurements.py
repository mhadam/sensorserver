from app.db.tables import Base
from sqlalchemy import func, Column, Integer, TIMESTAMP, String, Numeric


class Measurements(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True)
    created_at = Column(
        "created_at",
        TIMESTAMP(),
        nullable=False,
        default=func.now(),
        server_default=func.now(),
    )
    device_id = Column(String(length=6), index=True)
    co2 = Column(Integer())
    temperature = Column(Numeric(precision=4, scale=2))
    pm2_5 = Column(Integer())
    humidity = Column(Integer())
