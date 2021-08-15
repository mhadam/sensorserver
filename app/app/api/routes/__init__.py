from fastapi import APIRouter

from app.api.routes.measurements import router as measurements_router


router = APIRouter()


router.include_router(measurements_router, tags=["measurements"])
