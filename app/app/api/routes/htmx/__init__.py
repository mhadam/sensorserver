from fastapi import APIRouter

from app.api.routes.htmx.devices import router as device_requests_router
from app.api.routes.htmx.graphs import router as graphs_router
from app.api.routes.htmx.current import router as current_router


router = APIRouter()


router.include_router(device_requests_router, tags=["device-requests"])
router.include_router(graphs_router, tags=["graphs"])
router.include_router(current_router, tags=["current"])
