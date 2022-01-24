from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.dependencies.files import css_files, root_files, js_files
from app.api.routes import router as api_router
from app.api.routes.pages import router as pages_router
from app.api.routes.htmx import router as htmx_router
from app.core import tasks


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
    app_.include_router(pages_router)

    app_.mount("/css", css_files, name="css")
    app_.mount("/js", js_files, name="js")
    app_.mount("", root_files, name="root_files")

    return app_


app = get_application()
