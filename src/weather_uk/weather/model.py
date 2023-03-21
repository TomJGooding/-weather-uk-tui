from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass
class Weather:
    weather_type: WeatherType
    precipitation_probability: float
    temp_celsius: float
    feels_like_temp_celsius: float
    wind_direction: str
    wind_speed_mph: float
    wind_gust_mph: float
    visibility: str
    humidity_percent: float
    max_uv_index: int


class WeatherType(Enum):
    """Met Office DataPoint weather type codes:
    https://www.metoffice.gov.uk/services/data/datapoint/code-definitions
    """

    CLEAR_NIGHT = 0
    SUNNY_DAY = 1
    PARTLY_CLOUDY_NIGHT = 2
    PARTLY_CLOUDY_DAY = 3
    NOT_USED = 4
    MIST = 5
    FOG = 6
    CLOUDY = 7
    OVERCAST = 8
    LIGHT_RAIN_SHOWER_NIGHT = 9
    LIGHT_RAIN_SHOWER_DAY = 10
    DRIZZLE = 11
    LIGHT_RAIN = 12
    HEAVY_RAIN_SHOWER_NIGHT = 13
    HEAVY_RAIN_SHOWER_DAY = 14
    HEAVY_RAIN = 15
    SLEET_SHOWER_NIGHT = 16
    SLEET_SHOWER_DAY = 17
    SLEET = 18
    HAIL_SHOWER_NIGHT = 19
    HAIL_SHOWER_DAY = 20
    HAIL = 21
    LIGHT_SNOW_SHOWER_NIGHT = 22
    LIGHT_SNOW_SHOWER_DAY = 23
    LIGHT_SNOW = 24
    HEAVY_SNOW_SHOWER_NIGHT = 25
    HEAVY_SNOW_SHOWER_DAY = 26
    HEAVY_SNOW = 27
    THUNDER_SHOWER_NIGHT = 28
    THUNDER_SHOWER_DAY = 29
    THUNDER = 30

    def __str__(self) -> str:
        weather_type: str = self.name.replace("_", " ").capitalize()
        if weather_type not in ("Sunny day", "Clear night"):
            for period in [" day", " night"]:
                weather_type = weather_type.replace(period, "")

        return weather_type
