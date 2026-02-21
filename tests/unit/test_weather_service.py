import pytest

from weather_api.services import WeatherService


class FakeWeatherClient:
    async def get_current_weather(self, city: str):
        return {"city": city, "temp": 25}


class FakeCache:
    def __init__(self):
        self.store = {}

    async def get(self, key):
        return self.store.get(key)

    async def set(self, key, value, ttl):
        self.store[key] = value


class FakeStorage:
    def __init__(self):
        self.saved = {}

    async def save(self, key, data):
        self.saved[key] = data
        return key


class FakeLogger:
    def __init__(self):
        self.events = []

    async def log_event(self, city, timestamp, storage_key):
        self.events.append((city, timestamp, storage_key))


@pytest.mark.asyncio
async def test_weather_service_cache_miss():
    client = FakeWeatherClient()
    cache = FakeCache()
    storage = FakeStorage()
    logger = FakeLogger()

    service = WeatherService(client, cache, storage, logger)

    result = await service.get_weather("Berlin")

    assert result["city"] == "Berlin"
    assert "berlin" in cache.store  # cached
    assert len(storage.saved) == 1
    assert len(logger.events) == 1


@pytest.mark.asyncio
async def test_weather_service_cache_hit():
    client = FakeWeatherClient()
    cache = FakeCache()
    storage = FakeStorage()
    logger = FakeLogger()

    cache.store["berlin"] = {"city": "Berlin", "temp": 30}

    service = WeatherService(client, cache, storage, logger)

    result = await service.get_weather("Berlin")

    assert result["temp"] == 30
    assert len(storage.saved) == 0  # should not call storage
    assert len(logger.events) == 0  # should not log
