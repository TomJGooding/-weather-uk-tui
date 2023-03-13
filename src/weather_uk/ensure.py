from weather_uk.ports.weather_api import AbstractWeatherApi


def valid_authentication(api: AbstractWeatherApi) -> None:
    return api.check_authentication()
