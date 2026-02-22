import logging

from fastapi import FastAPI

from weather_api.api import router as weather_router
from weather_api.config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:

    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
    )
    app.include_router(weather_router, prefix=settings.api_prefix)
    app.state.settings = settings

    return app


app = create_app()
