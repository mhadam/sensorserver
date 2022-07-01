from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import relationship

from app.db.tables import Base, timestamps


class Users(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    __table_args__ = (*timestamps(),)

    device_auths = relationship("DeviceAuth", backref="users", passive_deletes=True)
