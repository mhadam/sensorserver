from fastapi import APIRouter

from app.api.routes.devices import router as measurements_router
from app.api.routes.users import router as users_router


router = APIRouter()


router.include_router(measurements_router, tags=["measurements"])
router.include_router(users_router)
