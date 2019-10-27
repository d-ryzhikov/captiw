from typing import Optional

from aiohttp.web import Application, run_app

from .config import load_config
from .routes import routes

app = Application()
app.add_routes(routes)


def main(settings: Optional[dict] = None):
    """Launch web application"""
    conf = load_config(settings or {})
    run_app(app, host=conf["host"], port=conf["port"])
