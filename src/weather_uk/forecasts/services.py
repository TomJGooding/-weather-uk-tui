from weather_uk.data import models
from weather_uk.ports.weather_api import AbstractWeatherApi


def get_forecast(
    api: AbstractWeatherApi,
    location_id: int,
) -> list[models.ForecastDay]:
    return api.get_forecast(location_id)
