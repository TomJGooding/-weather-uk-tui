from pathlib import Path

from weather_uk import config
from weather_uk.ports.weather_api import AbstractWeatherApi


def config_file_exists(filepath: Path) -> None:
    if not filepath.is_file():
        filepath.parent.mkdir(parents=True, exist_ok=True)
        config.update_config(api_key="", filepath=filepath)


def valid_authentication(api: AbstractWeatherApi) -> None:
    return api.check_authentication()
