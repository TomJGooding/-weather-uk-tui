from weather_uk.data import models
from weather_uk.ports.weather_api import AbstractWeatherApi


def get_locations_list(api: AbstractWeatherApi) -> list[models.Location]:
    return api.get_locations_list()
