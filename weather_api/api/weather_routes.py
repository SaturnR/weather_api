import logging

from fastapi import APIRouter, Depends, Query

from weather_api.config import settings
from weather_api.dependencies import get_weather_service
from weather_api.services.weather_service import WeatherService

router = APIRouter(prefix=f"{settings.base_url}/weather-today", tags=["Weather"])

logger = logging.getLogger(__name__)


@router.get("")
async def get_weather(
    city: str = Query(..., description="City name"),
    service: WeatherService = Depends(get_weather_service),
):
    return await service.get_weather(city)
