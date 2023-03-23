import configparser
from dataclasses import dataclass
from pathlib import Path

import platformdirs

from weather_uk import ensure

APPNAME = "weather-uk"
USER_CONFIG_PATH = platformdirs.user_config_path(APPNAME)
CONFIG_FILEPATH = Path(USER_CONFIG_PATH / "weather-uk.cfg")


@dataclass
class UserConfig:
    api_key: str


def load_config(filepath: Path = CONFIG_FILEPATH) -> UserConfig:
    ensure.config_file_exists(filepath)

    config = configparser.ConfigParser()
    config.read(filepath)

    api_key = config["weather_api"]["api_key"]
    return UserConfig(api_key)


def update_config(
    api_key: str,
    filepath: Path = CONFIG_FILEPATH,
) -> UserConfig:
    config = configparser.ConfigParser()
    config.read(filepath)

    if "weather_api" not in config:
        config["weather_api"] = {}

    config["weather_api"]["api_key"] = api_key

    with open(filepath, "w") as configfile:
        config.write(configfile)

    return load_config(filepath)
