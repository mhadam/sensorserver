from app.db.tables import Base
from fastapi_users.db import SQLAlchemyBaseUserTable


# class Users(Base):
#     __tablename__ = "users"
#     __table__ = Table(
#         "users",
#         Base.metadata,
#         Column("id", Integer, primary_key=True),
#         Column("username", Text, unique=True, nullable=False, index=True),
#         Column("email", Text, unique=True, nullable=False, index=True),
#         Column("email_verified", Boolean, nullable=False, server_default="False"),
#         Column("salt", Text, nullable=False),
#         Column("password", Text, nullable=False),
#         Column("is_active", Boolean, nullable=False, server_default="True"),
#         Column("is_superuser", Boolean, nullable=False, server_default="False"),
#         *timestamps()
#     )
#
#     device_auths = relationship("DeviceAuth", backref="users")


class Users(Base, SQLAlchemyBaseUserTable):
    __tablename__ = "users"
