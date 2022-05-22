from fastapi import APIRouter
from starlette.requests import Request

from app.api.dependencies.auth import fastapi_users
from app.api.dependencies.files import templates

current_user = fastapi_users.current_user(active=True)

router = APIRouter(include_in_schema=False)


@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


@router.get("/graphs.html")
async def index(request: Request):
    return templates.TemplateResponse("graphs.html", context={"request": request})


@router.get("/devices.html")
async def index(request: Request):
    return templates.TemplateResponse("devices.html", context={"request": request})


@router.get("/current.html")
async def current(request: Request):
    return templates.TemplateResponse("current.html", context={"request": request})
