from weather_uk.locations.model import Location
from weather_uk.ports.weather_api import AbstractWeatherApi


def get_locations_list(api: AbstractWeatherApi) -> list[Location]:
    return api.get_locations_list()
