import logging

import httpx
import pytest

logger = logging.getLogger(__name__)

BASE_URL = "http://api:8000"


@pytest.mark.asyncio
async def test_weather_e2e_real_stack():
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        response = await client.get(
            "/api/v1/weather-today",
            params={"city": "Berlin"},
        )

    assert response.status_code == 200

    data = response.json()
    assert "name" in data
    assert data["name"].lower() == "berlin"
