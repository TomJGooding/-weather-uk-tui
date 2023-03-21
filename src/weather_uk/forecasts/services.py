from weather_uk.forecasts.models import ForecastDay
from weather_uk.ports.weather_api import AbstractWeatherApi


def get_forecast(
    api: AbstractWeatherApi,
    location_id: int,
) -> list[ForecastDay]:
    return api.get_forecast(location_id)
