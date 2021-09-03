from app.core.config import DATABASE_URL
from databases import Database

database = Database(DATABASE_URL, min_size=2, max_size=10)