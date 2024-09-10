from weather_uk.data import models
from weather_uk.domain.weather_api_client import AbstractWeatherAPIClient


def get_forecast(
    api_client: AbstractWeatherAPIClient,
    location_id: int,
) -> list[models.ForecastDay]:
    return api_client.get_forecast(location_id)
