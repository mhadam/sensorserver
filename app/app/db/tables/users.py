from sqlalchemy.orm import relationship

from app.db.tables import Base, timestamps
from fastapi_users.db import SQLAlchemyBaseUserTable


class Users(Base, SQLAlchemyBaseUserTable):
    __tablename__ = "users"
    __table_args__ = (*timestamps(),)

    device_auths = relationship("DeviceAuth", backref="users", passive_deletes=True)
