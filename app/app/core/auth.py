from app.core.config import SECRET_KEY
from fastapi_users.authentication import CookieAuthentication

cookie_authentication = CookieAuthentication(secret=SECRET_KEY, lifetime_seconds=3600)

auth_backends = [cookie_authentication]
