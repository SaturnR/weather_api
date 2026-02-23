import logging

from fastapi import APIRouter, Depends, Query

from weather_api.dependencies import get_weather_service
from weather_api.services.weather_service import WeatherService

router = APIRouter(prefix="/weather-today", tags=["Weather"])

logger = logging.getLogger(__name__)


@router.get("")
async def get_weather(
    city: str = Query(..., description="City name", min_length=1),
    service: WeatherService = Depends(get_weather_service),
):
    logger.debug("*********************************")

    return await service.get_weather(city)
