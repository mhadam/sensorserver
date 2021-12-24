from starlette.templating import Jinja2Templates

from app.api.routes import router as api_router
from app.api.routes.htmx import router as htmx_router
from app.core import tasks
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


def get_application() -> FastAPI:
    app_ = FastAPI(title="sensorserver", version="0.1.0")
    app_.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app_.add_event_handler("startup", tasks.create_start_app_handler(app_))
    app_.add_event_handler("shutdown", tasks.create_stop_app_handler(app_))

    app_.include_router(htmx_router, prefix="/htmx")
    app_.include_router(api_router, prefix="/api")

    return app_


templates = Jinja2Templates(directory="templates")

app = get_application()
