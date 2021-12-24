from fastapi import APIRouter

from app.api.routes.htmx.allow_devices import router as allow_devices_router


router = APIRouter()


router.include_router(allow_devices_router, tags=["allow_devices"])
