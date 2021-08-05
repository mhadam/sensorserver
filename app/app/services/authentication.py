import bcrypt
from passlib.context import CryptContext

from app.models.user import UserPasswordUpdate


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthException(BaseException):
    """
    Custom auth exception that can be modified later on.
    """

    pass


def hash_password_with_salt(plaintext_password: str) -> UserPasswordUpdate:
    salt = bcrypt.gensalt().decode()
    hashed_password = pwd_context.hash(plaintext_password + salt)
    return UserPasswordUpdate(salt=salt, password=hashed_password)
