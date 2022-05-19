from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from pathlib import Path

from app import BASE_DIR

templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))

static_dir = str(Path(BASE_DIR, "static"))
css_files = StaticFiles(directory=static_dir + "/css")
js_files = StaticFiles(directory=static_dir + "/js")
# root_files includes html and images, etc.
# root means at _root_ path of website
# root_files = StaticFiles(html=True, packages=[('app.static.images', ''), ('app.static.html', '')])
root_files = StaticFiles(html=True, packages=["app.static.images", "app.static.html"])
