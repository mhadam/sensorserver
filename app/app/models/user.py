from app.models.core import CoreModel


class UserPasswordUpdate(CoreModel):
    salt: str
    password: str
