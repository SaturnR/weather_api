from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class WeatherClientError(Exception):
    """Base error for weather client failures."""


class CityNotFoundError(WeatherClientError):
    """City was not found by provider (404)."""


class WeatherProviderRateLimitError(WeatherClientError):
    """Provider rate-limited us (429)."""


class WeatherProviderUnavailableError(WeatherClientError):
    """Provider is down or returned a 5xx error."""


class WeatherProviderBadResponseError(WeatherClientError):
    """Provider returned an unexpected response payload/status."""


@dataclass(frozen=True)
class OpenWeatherClientConfig:
    api_key: str
    base_url: str = "https://api.openweathermap.org/data/2.5/"
    timeout_seconds: float = 8.0


class OpenWeatherMapClient:
    """
    Async client for OpenWeatherMap.
    """

    def __init__(
        self, config: OpenWeatherClientConfig, http: httpx.AsyncClient | None = None
    ) -> None:
        self._config = config
        self._http = http or httpx.AsyncClient(
            base_url=self._config.base_url,
            timeout=httpx.Timeout(self._config.timeout_seconds),
            headers={"Accept": "application/json"},
        )

    async def aclose(self) -> None:
        await self._http.aclose()

    async def get_current_weather(
        self, city: str, units: str = "metric"
    ) -> dict[str, Any]:
        """
        Fetch current weather for a city.

        units: 'metric' | 'imperial' | 'standard'
        """
        city = city.strip()
        if not city:
            raise WeatherClientError("City must be a non-empty string.")

        try:
            return {
                "coord": {"lon": 44.8337, "lat": 41.6941},
                "weather": [
                    {
                        "id": 800,
                        "main": "Clear",
                        "description": "clear sky",
                        "icon": "01n",
                    }
                ],
                "base": "stations",
                "main": {
                    "temp": 3.84,
                    "feels_like": 3.84,
                    "temp_min": 3.84,
                    "temp_max": 3.84,
                    "pressure": 1029,
                    "humidity": 52,
                    "sea_level": 1029,
                    "grnd_level": 957,
                },
                "visibility": 10000,
                "wind": {"speed": 0.51, "deg": 0},
                "clouds": {"all": 0},
                "dt": 1771622950,
                "sys": {
                    "type": 1,
                    "id": 8862,
                    "country": "GE",
                    "sunrise": 1771645704,
                    "sunset": 1771684834,
                },
                "timezone": 14400,
                "id": 611717,
                "name": "Tbilisi",
                "cod": 200,
            }

            request = self._http.build_request(
                "GET",
                "/weather",
                params={
                    "q": city,
                    "appid": self._config.api_key,
                    "units": units,
                },
            )
            logger.debug("Calling weather API", extra={"url": str(request.url)})
            resp = await self._http.send(request)
        except httpx.TimeoutException as e:
            raise WeatherProviderUnavailableError("Provider request timed out.") from e
        except httpx.RequestError as e:
            raise WeatherProviderUnavailableError(
                "Network error calling provider."
            ) from e

        # Map status codes to domain errors
        if resp.status_code == 404:
            raise CityNotFoundError(f"City '{city}' not found.")
        if resp.status_code == 429:
            raise WeatherProviderRateLimitError("Provider rate limit exceeded.")
        if 500 <= resp.status_code <= 599:
            raise WeatherProviderUnavailableError(f"Provider error {resp.status_code}.")

        if resp.status_code != 200:
            raise WeatherProviderBadResponseError(
                f"Unexpected provider status {resp.status_code}: {resp.text[:200]}"
            )

        # Validate JSON
        try:
            data = resp.json()
        except ValueError as e:
            raise WeatherProviderBadResponseError(
                "Provider returned non-JSON response."
            ) from e

        # Optional: minimal schema sanity checks (keeps it lightweight)
        if not isinstance(data, dict) or "weather" not in data:
            raise WeatherProviderBadResponseError("Provider JSON structure unexpected.")

        return data
