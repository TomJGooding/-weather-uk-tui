from weather_uk.data import models
from weather_uk.domain.weather_api_client import AbstractWeatherAPIClient


def get_locations_list(
    api_client: AbstractWeatherAPIClient,
) -> list[models.Location]:
    return api_client.get_locations_list()
