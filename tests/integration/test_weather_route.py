import httpx
import pytest
from httpx import AsyncClient

from weather_api.providers import CityNotFoundError


class FakeFailingWeatherService:
    async def get_weather(self, city: str):
        raise CityNotFoundError("not found")


@pytest.mark.asyncio
async def test_weather_endpoint_city_not_found(app):
    # override with failing service
    from weather_api.dependencies import get_weather_service

    app.dependency_overrides[get_weather_service] = lambda: FakeFailingWeatherService()
    transport = httpx.ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/weather", params={"city": "NopeCity"})

    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_weather_endpoint_success(app):
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        resp = await client.get("/api/v1/weather-today", params={"city": "Berlin"})

    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_weather_endpoint_validation_error(app):
    transport = httpx.ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/weather-today", params={"city": ""})

    # FastAPI/Pydantic validation error
    assert resp.status_code in (400, 422)
