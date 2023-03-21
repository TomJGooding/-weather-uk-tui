import datetime
import json
from typing import Any

from weather_uk.forecasts.models import ForecastDay, ForecastHour
from weather_uk.locations.model import Location
from weather_uk.weather.model import Weather, WeatherType


class NumbersStoredAsTextDecoder(json.JSONDecoder):
    def decode(self, s: Any, *args: Any, **kwargs: Any) -> Any:
        result = super().decode(s, *args, **kwargs)
        return self._decode(result)

    def _decode(self, o: Any) -> Any:
        if isinstance(o, str):
            try:
                return int(o)
            except ValueError:
                try:
                    return float(o)
                except ValueError:
                    return o
        elif isinstance(o, dict):
            return {k: self._decode(v) for k, v in o.items()}
        elif isinstance(o, list):
            return [self._decode(v) for v in o]
        else:
            return o


def decode_met_office_locations(json_data: dict) -> list[Location]:
    locations: list[Location] = []
    locations_data: list[dict] = json_data["Locations"]["Location"]
    for location in locations_data:
        id: int = location["id"]
        name: str = location["name"]
        region: str | None = location.get("unitaryAuthArea")

        locations.append(Location(id, name, region))

    return locations


def decode_met_office_forecast(json_data: dict) -> list[ForecastDay]:
    forecast: list[ForecastDay] = []
    forecast_data: dict = json_data["SiteRep"]["DV"]
    for day in forecast_data["Location"]["Period"]:
        # requires slice as datetime doesn't parse the "Z" from ISO 8601
        date = datetime.date.fromisoformat(day["value"][:-1])
        forecast_day = ForecastDay(date=date, hours=[])
        for period in day["Rep"]:
            weather: Weather = decode_met_office_weather(period)
            minutes_after_midnight: int = period["$"]
            hour = datetime.time(minutes_after_midnight // 60)
            forecast_day.hours.append(ForecastHour(hour, weather))

        forecast.append(forecast_day)

    return forecast


def decode_met_office_weather(json_data: dict) -> Weather:
    return Weather(
        weather_type=WeatherType(json_data["W"]),
        precipitation_probability=json_data["Pp"],
        temp_celsius=json_data["T"],
        feels_like_temp_celsius=json_data["F"],
        wind_direction=json_data["D"],
        wind_speed_mph=json_data["S"],
        wind_gust_mph=json_data["G"],
        visibility=json_data["V"],
        humidity_percent=json_data["H"],
        max_uv_index=json_data["U"],
    )
