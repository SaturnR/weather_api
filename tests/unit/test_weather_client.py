import httpx
import pytest

from weather_api.providers import (
    CityNotFoundError,
    OpenWeatherClientConfig,
    OpenWeatherMapClient,
)


@pytest.mark.asyncio
async def test_weather_client_success():
    async def mock_handler(request: httpx.Request):
        assert request.url.path == "/weather"
        return httpx.Response(
            status_code=200,
            json={"weather": [{"main": "Clear"}]},
        )

    transport = httpx.MockTransport(mock_handler)

    async with httpx.AsyncClient(
        transport=transport,
        base_url="https://api.test.com",
    ) as mock_http:
        client = OpenWeatherMapClient(
            config=OpenWeatherClientConfig(
                api_key="test",
                base_url="https://api.test.com",
            ),
            http=mock_http,
        )

        result = await client.get_current_weather("Berlin")

        assert result["weather"][0]["main"] == "Clear"


@pytest.mark.asyncio
async def test_weather_client_city_not_found():
    async def mock_handler(request: httpx.Request):
        return httpx.Response(status_code=404)

    transport = httpx.MockTransport(mock_handler)

    async with httpx.AsyncClient(
        transport=transport,
        base_url="https://api.test.com",
    ) as mock_http:
        client = OpenWeatherMapClient(
            config=OpenWeatherClientConfig(
                api_key="test",
                base_url="https://api.test.com",
            ),
            http=mock_http,
        )

        with pytest.raises(CityNotFoundError):
            await client.get_current_weather("UnknownCity")
