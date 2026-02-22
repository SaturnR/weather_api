# tests/integration/conftest.py
import logging

import pytest
from fastapi import FastAPI

from weather_api.dependencies import get_weather_service
from weather_api.main import create_app

logger = logging.getLogger(__name__)


class FakeWeatherService:
    async def get_weather(self, city: str):
        return {"city": city, "source": "fake", "temp": 21}


@pytest.fixture
def app() -> FastAPI:
    app = create_app()
    app.dependency_overrides[get_weather_service] = lambda: FakeWeatherService()
    return app
