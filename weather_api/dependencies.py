from functools import lru_cache

from redis.asyncio import Redis

from weather_api.cache import RedisCache
from weather_api.config import settings
from weather_api.event_logging import (
    DynamoDBEventLogger,
    EventLogger,
    SQLiteEventLogger,
)
from weather_api.providers import (
    OpenWeatherClientConfig,
    OpenWeatherMapClient,
)
from weather_api.services import WeatherService
from weather_api.storage import MinioStorage, S3Storage, Storage

weather_client = OpenWeatherMapClient(
    config=OpenWeatherClientConfig(
        api_key=settings.openweather_api_key,
        base_url=settings.openweather_base_url,
    )
)


@lru_cache
def get_event_logger() -> EventLogger:
    if settings.environment == "local":
        return SQLiteEventLogger(db_path="data/events.db")

    return DynamoDBEventLogger(
        region=settings.aws_region,
        access_key=settings.aws_access_key,
        secret_key=settings.aws_secret_key,
        table_name=settings.dynamodb_table,
    )


def get_weather_service() -> WeatherService:

    cache = RedisCache(settings.redis_url)
    storage = MinioStorage(
        endpoint=settings.minio_endpoint,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        bucket=settings.minio_bucket,
    )

    logger = get_event_logger()
    return WeatherService(weather_client, cache, storage, logger)


async def get_redis() -> Redis:
    redis = Redis.from_url(
        settings.redis_url,
        decode_responses=True,
    )
    return redis


def get_storage() -> Storage:
    if settings.environment == "local":
        return MinioStorage(
            endpoint=settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            bucket=settings.minio_bucket,
        )

    return S3Storage(
        region=settings.aws_region,
        access_key=settings.aws_access_key,
        secret_key=settings.aws_secret_key,
        bucket=settings.s3_bucket,
    )
