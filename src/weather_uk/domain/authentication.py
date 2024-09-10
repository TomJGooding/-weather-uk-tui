from weather_uk.domain.weather_api_client import AbstractWeatherAPIClient


def check_valid_authentication(api_client: AbstractWeatherAPIClient) -> None:
    return api_client.check_authentication()
