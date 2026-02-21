from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
    )

    app_name: str = "Weather API"
    base_url: str = "/weather"
    environment: str = "local"
    openweather_api_key: str
    openweather_base_url: str = "https://api.openweathermap.org/data/2.5"

    redis_url: str

    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket: str = "weather-data"

    cache_ttl_seconds: int = 300


settings = Settings()
