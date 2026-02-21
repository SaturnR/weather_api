from datetime import datetime

from weather_api.dependencies import settings
from weather_api.event_logging import EventLogger
from weather_api.providers import OpenWeatherMapClient


class WeatherService:
    def __init__(
        self,
        weather_client,
        cache,
        storage,
        logger: EventLogger,
    ):
        self._weather_client: OpenWeatherMapClient = weather_client
        self._cache = cache
        self._storage = storage
        self._logger = logger

    async def get_weather(self, city: str):
        city_key = city.lower().strip()

        # cached = await self._cache.get(city_key)
        # if cached:
        #    return cached

        weather_data = await self._weather_client.get_current_weather(city)

        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        filename = f"{city_key}_{timestamp}.json"

        await self._storage.save(filename, weather_data)

        # 🔥 NEW PART
        await self._logger.log_event(city, timestamp, filename)

        await self._cache.set(city_key, weather_data, ttl=settings.cache_ttl_seconds)

        return weather_data
