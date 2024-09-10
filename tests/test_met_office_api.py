import datetime
import json
from pathlib import Path
from typing import Optional

import requests

from weather_uk.data import models
from weather_uk.domain import serialisers
from weather_uk.domain.weather_api_client import AbstractWeatherAPIClient

FAKE_DATA_DIR = Path(__file__).parent / "data"


class FakeMetOfficeAPIClient(AbstractWeatherAPIClient):
    BASE_URL: str = "http://datapoint.metoffice.gov.uk/public/data/"
    DATATYPE: str = "json"

    def __init__(self, api_key: str) -> None:
        self.api_key: str = api_key

    def _fake_request(self, resource: str) -> str:
        filename: str = resource
        return (FAKE_DATA_DIR / filename).read_text()

    def check_authentication(self) -> None:
        pass

    def get_locations_list(self) -> list[models.Location]:
        resource: str = "sitelist"
        resp: str = self._fake_request(resource)
        json_data: dict = json.loads(
            resp,
            cls=serialisers.NumbersStoredAsTextDecoder,
        )

        return serialisers.decode_met_office_locations(json_data)

    def get_forecast(self, location_id: int) -> list[models.ForecastDay]:
        resource: str = f"{location_id}-3hourly"
        resp: str = self._fake_request(resource)
        json_data = json.loads(resp, cls=serialisers.NumbersStoredAsTextDecoder)

        return serialisers.decode_met_office_forecast(json_data)

    def _build_request(
        self, resource: str, query: Optional[str] = None
    ) -> requests.Request:
        query = "" if not query else query
        url: str = f"{self.BASE_URL}{resource}?{query}key={self.api_key}"
        return requests.Request(method="GET", url=url)


def test_build_request_without_query() -> None:
    api_key: str = "01234567-89ab-cdef-0123-456789abcdef"
    api = FakeMetOfficeAPIClient(api_key)
    resource: str = "val/wxfcs/all/json/sitelist"

    assert api._build_request(resource).method == "GET"
    assert api._build_request(resource).url == (
        "http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/sitelist"
        "?key=01234567-89ab-cdef-0123-456789abcdef"
    )


def test_build_request_with_query() -> None:
    api_key: str = "01234567-89ab-cdef-0123-456789abcdef"
    api = FakeMetOfficeAPIClient(api_key)
    resource: str = "val/wxfcs/all/json/310069"
    query: str = "res=3hourly&"

    assert api._build_request(resource, query).url == (
        "http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/310069"
        "?res=3hourly&key=01234567-89ab-cdef-0123-456789abcdef"
    )


def test_get_locations_list() -> None:
    api_key: str = "01234567-89ab-cdef-0123-456789abcdef"
    api = FakeMetOfficeAPIClient(api_key)

    expected: list[models.Location] = [
        models.Location(14, "Carlisle Airport", "Cumbria"),
        models.Location(26, "Liverpool John Lennon Airport", "Merseyside"),
        models.Location(33, "Scatsta", "Shetland Islands"),
        models.Location(3066, "Kinloss", "Moray"),
        models.Location(3068, "Lossiemouth", "Moray"),
        models.Location(3075, "Wick John O Groats Airport", "Highland"),
        models.Location(3081, "Braemar", "Aberdeenshire"),
        models.Location(3002, "Baltasound", "Shetland Islands"),
        models.Location(3005, "Lerwick (S. Screen)", "Shetland Islands"),
        models.Location(3008, "Fair Isle", "Shetland Islands"),
    ]

    actual: list[models.Location] = api.get_locations_list()

    assert actual == expected


def test_get_forecast() -> None:
    api_key: str = "01234567-89ab-cdef-0123-456789abcdef"
    api = FakeMetOfficeAPIClient(api_key)

    actual: list[models.ForecastDay] = api.get_forecast(location_id=310069)

    assert len(actual) == 5

    expected = [
        models.ForecastDay(
            date=datetime.date(2023, 3, 13),
            hours=[
                models.ForecastHour(
                    time=datetime.time(18, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.CLOUDY,
                        precipitation_probability=29,
                        temp_celsius=11,
                        feels_like_temp_celsius=8,
                        wind_direction="SW",
                        wind_speed_mph=13,
                        wind_gust_mph=29,
                        visibility="VG",
                        humidity_percent=81,
                        max_uv_index=1,
                    ),
                ),
                models.ForecastHour(
                    time=datetime.time(21, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.LIGHT_RAIN,
                        precipitation_probability=45,
                        temp_celsius=10,
                        feels_like_temp_celsius=8,
                        wind_direction="SW",
                        wind_speed_mph=9,
                        wind_gust_mph=20,
                        visibility="MO",
                        humidity_percent=93,
                        max_uv_index=0,
                    ),
                ),
            ],
        ),
        models.ForecastDay(
            date=datetime.date(2023, 3, 14),
            hours=[
                models.ForecastHour(
                    time=datetime.time(0, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.CLOUDY,
                        precipitation_probability=55,
                        temp_celsius=8,
                        feels_like_temp_celsius=4,
                        wind_direction="NW",
                        wind_speed_mph=18,
                        wind_gust_mph=36,
                        visibility="GO",
                        humidity_percent=82,
                        max_uv_index=0,
                    ),
                ),
                models.ForecastHour(
                    time=datetime.time(3, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.CLOUDY,
                        precipitation_probability=16,
                        temp_celsius=6,
                        feels_like_temp_celsius=2,
                        wind_direction="WNW",
                        wind_speed_mph=13,
                        wind_gust_mph=31,
                        visibility="EX",
                        humidity_percent=73,
                        max_uv_index=0,
                    ),
                ),
                models.ForecastHour(
                    time=datetime.time(6, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.LIGHT_RAIN_SHOWER_NIGHT,
                        precipitation_probability=85,
                        temp_celsius=5,
                        feels_like_temp_celsius=1,
                        wind_direction="WNW",
                        wind_speed_mph=11,
                        wind_gust_mph=22,
                        visibility="GO",
                        humidity_percent=83,
                        max_uv_index=0,
                    ),
                ),
                models.ForecastHour(
                    time=datetime.time(9, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.CLOUDY,
                        precipitation_probability=9,
                        temp_celsius=6,
                        feels_like_temp_celsius=3,
                        wind_direction="NW",
                        wind_speed_mph=11,
                        wind_gust_mph=22,
                        visibility="VG",
                        humidity_percent=73,
                        max_uv_index=1,
                    ),
                ),
                models.ForecastHour(
                    time=datetime.time(12, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.SUNNY_DAY,
                        precipitation_probability=2,
                        temp_celsius=9,
                        feels_like_temp_celsius=6,
                        wind_direction="NW",
                        wind_speed_mph=11,
                        wind_gust_mph=20,
                        visibility="EX",
                        humidity_percent=48,
                        max_uv_index=3,
                    ),
                ),
                models.ForecastHour(
                    time=datetime.time(15, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.SUNNY_DAY,
                        precipitation_probability=4,
                        temp_celsius=10,
                        feels_like_temp_celsius=7,
                        wind_direction="WNW",
                        wind_speed_mph=11,
                        wind_gust_mph=22,
                        visibility="EX",
                        humidity_percent=43,
                        max_uv_index=2,
                    ),
                ),
                models.ForecastHour(
                    time=datetime.time(18, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.SUNNY_DAY,
                        precipitation_probability=31,
                        temp_celsius=7,
                        feels_like_temp_celsius=4,
                        wind_direction="W",
                        wind_speed_mph=9,
                        wind_gust_mph=20,
                        visibility="EX",
                        humidity_percent=61,
                        max_uv_index=1,
                    ),
                ),
                models.ForecastHour(
                    time=datetime.time(21, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.LIGHT_RAIN_SHOWER_NIGHT,
                        precipitation_probability=37,
                        temp_celsius=5,
                        feels_like_temp_celsius=3,
                        wind_direction="W",
                        wind_speed_mph=7,
                        wind_gust_mph=16,
                        visibility="VG",
                        humidity_percent=80,
                        max_uv_index=0,
                    ),
                ),
            ],
        ),
        models.ForecastDay(
            date=datetime.date(2023, 3, 15),
            hours=[
                models.ForecastHour(
                    time=datetime.time(0, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.PARTLY_CLOUDY_NIGHT,
                        precipitation_probability=5,
                        temp_celsius=5,
                        feels_like_temp_celsius=3,
                        wind_direction="W",
                        wind_speed_mph=4,
                        wind_gust_mph=11,
                        visibility="VG",
                        humidity_percent=83,
                        max_uv_index=0,
                    ),
                ),
                models.ForecastHour(
                    time=datetime.time(3, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.CLOUDY,
                        precipitation_probability=3,
                        temp_celsius=3,
                        feels_like_temp_celsius=2,
                        wind_direction="W",
                        wind_speed_mph=2,
                        wind_gust_mph=7,
                        visibility="VG",
                        humidity_percent=85,
                        max_uv_index=0,
                    ),
                ),
                models.ForecastHour(
                    time=datetime.time(6, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.CLOUDY,
                        precipitation_probability=7,
                        temp_celsius=3,
                        feels_like_temp_celsius=2,
                        wind_direction="S",
                        wind_speed_mph=2,
                        wind_gust_mph=4,
                        visibility="GO",
                        humidity_percent=88,
                        max_uv_index=0,
                    ),
                ),
                models.ForecastHour(
                    time=datetime.time(9, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.CLOUDY,
                        precipitation_probability=50,
                        temp_celsius=6,
                        feels_like_temp_celsius=4,
                        wind_direction="SE",
                        wind_speed_mph=4,
                        wind_gust_mph=9,
                        visibility="GO",
                        humidity_percent=82,
                        max_uv_index=1,
                    ),
                ),
                models.ForecastHour(
                    time=datetime.time(12, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.HEAVY_RAIN,
                        precipitation_probability=84,
                        temp_celsius=8,
                        feels_like_temp_celsius=5,
                        wind_direction="SSE",
                        wind_speed_mph=11,
                        wind_gust_mph=20,
                        visibility="GO",
                        humidity_percent=84,
                        max_uv_index=1,
                    ),
                ),
                models.ForecastHour(
                    time=datetime.time(15, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.HEAVY_RAIN,
                        precipitation_probability=84,
                        temp_celsius=8,
                        feels_like_temp_celsius=5,
                        wind_direction="SSE",
                        wind_speed_mph=11,
                        wind_gust_mph=25,
                        visibility="MO",
                        humidity_percent=88,
                        max_uv_index=1,
                    ),
                ),
                models.ForecastHour(
                    time=datetime.time(18, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.HEAVY_RAIN,
                        precipitation_probability=83,
                        temp_celsius=9,
                        feels_like_temp_celsius=7,
                        wind_direction="S",
                        wind_speed_mph=11,
                        wind_gust_mph=25,
                        visibility="MO",
                        humidity_percent=92,
                        max_uv_index=1,
                    ),
                ),
                models.ForecastHour(
                    time=datetime.time(21, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.HEAVY_RAIN,
                        precipitation_probability=83,
                        temp_celsius=10,
                        feels_like_temp_celsius=7,
                        wind_direction="S",
                        wind_speed_mph=13,
                        wind_gust_mph=25,
                        visibility="MO",
                        humidity_percent=94,
                        max_uv_index=0,
                    ),
                ),
            ],
        ),
        models.ForecastDay(
            date=datetime.date(2023, 3, 16),
            hours=[
                models.ForecastHour(
                    time=datetime.time(0, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.LIGHT_RAIN,
                        precipitation_probability=56,
                        temp_celsius=11,
                        feels_like_temp_celsius=8,
                        wind_direction="S",
                        wind_speed_mph=13,
                        wind_gust_mph=27,
                        visibility="GO",
                        humidity_percent=93,
                        max_uv_index=0,
                    ),
                ),
                models.ForecastHour(
                    time=datetime.time(3, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.OVERCAST,
                        precipitation_probability=19,
                        temp_celsius=11,
                        feels_like_temp_celsius=8,
                        wind_direction="SSW",
                        wind_speed_mph=16,
                        wind_gust_mph=31,
                        visibility="GO",
                        humidity_percent=91,
                        max_uv_index=0,
                    ),
                ),
                models.ForecastHour(
                    time=datetime.time(6, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.LIGHT_RAIN_SHOWER_NIGHT,
                        precipitation_probability=33,
                        temp_celsius=11,
                        feels_like_temp_celsius=8,
                        wind_direction="S",
                        wind_speed_mph=16,
                        wind_gust_mph=31,
                        visibility="MO",
                        humidity_percent=92,
                        max_uv_index=0,
                    ),
                ),
                models.ForecastHour(
                    time=datetime.time(9, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.LIGHT_RAIN,
                        precipitation_probability=48,
                        temp_celsius=11,
                        feels_like_temp_celsius=8,
                        wind_direction="S",
                        wind_speed_mph=18,
                        wind_gust_mph=31,
                        visibility="MO",
                        humidity_percent=90,
                        max_uv_index=1,
                    ),
                ),
                models.ForecastHour(
                    time=datetime.time(12, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.HEAVY_RAIN,
                        precipitation_probability=68,
                        temp_celsius=11,
                        feels_like_temp_celsius=8,
                        wind_direction="S",
                        wind_speed_mph=16,
                        wind_gust_mph=29,
                        visibility="MO",
                        humidity_percent=88,
                        max_uv_index=1,
                    ),
                ),
                models.ForecastHour(
                    time=datetime.time(15, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.LIGHT_RAIN,
                        precipitation_probability=48,
                        temp_celsius=12,
                        feels_like_temp_celsius=10,
                        wind_direction="SSW",
                        wind_speed_mph=13,
                        wind_gust_mph=25,
                        visibility="MO",
                        humidity_percent=90,
                        max_uv_index=1,
                    ),
                ),
                models.ForecastHour(
                    time=datetime.time(18, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.OVERCAST,
                        precipitation_probability=19,
                        temp_celsius=12,
                        feels_like_temp_celsius=9,
                        wind_direction="SSW",
                        wind_speed_mph=11,
                        wind_gust_mph=20,
                        visibility="GO",
                        humidity_percent=93,
                        max_uv_index=1,
                    ),
                ),
                models.ForecastHour(
                    time=datetime.time(21, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.OVERCAST,
                        precipitation_probability=15,
                        temp_celsius=11,
                        feels_like_temp_celsius=9,
                        wind_direction="SSW",
                        wind_speed_mph=9,
                        wind_gust_mph=18,
                        visibility="GO",
                        humidity_percent=94,
                        max_uv_index=0,
                    ),
                ),
            ],
        ),
        models.ForecastDay(
            date=datetime.date(2023, 3, 17),
            hours=[
                models.ForecastHour(
                    time=datetime.time(0, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.OVERCAST,
                        precipitation_probability=13,
                        temp_celsius=11,
                        feels_like_temp_celsius=9,
                        wind_direction="S",
                        wind_speed_mph=9,
                        wind_gust_mph=18,
                        visibility="GO",
                        humidity_percent=95,
                        max_uv_index=0,
                    ),
                ),
                models.ForecastHour(
                    time=datetime.time(3, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.OVERCAST,
                        precipitation_probability=12,
                        temp_celsius=11,
                        feels_like_temp_celsius=9,
                        wind_direction="S",
                        wind_speed_mph=9,
                        wind_gust_mph=18,
                        visibility="GO",
                        humidity_percent=95,
                        max_uv_index=0,
                    ),
                ),
                models.ForecastHour(
                    time=datetime.time(6, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.OVERCAST,
                        precipitation_probability=14,
                        temp_celsius=11,
                        feels_like_temp_celsius=8,
                        wind_direction="S",
                        wind_speed_mph=11,
                        wind_gust_mph=18,
                        visibility="GO",
                        humidity_percent=95,
                        max_uv_index=0,
                    ),
                ),
                models.ForecastHour(
                    time=datetime.time(9, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.CLOUDY,
                        precipitation_probability=18,
                        temp_celsius=11,
                        feels_like_temp_celsius=9,
                        wind_direction="S",
                        wind_speed_mph=11,
                        wind_gust_mph=22,
                        visibility="MO",
                        humidity_percent=94,
                        max_uv_index=1,
                    ),
                ),
                models.ForecastHour(
                    time=datetime.time(12, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.LIGHT_RAIN_SHOWER_DAY,
                        precipitation_probability=39,
                        temp_celsius=13,
                        feels_like_temp_celsius=10,
                        wind_direction="S",
                        wind_speed_mph=13,
                        wind_gust_mph=25,
                        visibility="GO",
                        humidity_percent=87,
                        max_uv_index=2,
                    ),
                ),
                models.ForecastHour(
                    time=datetime.time(15, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.LIGHT_RAIN_SHOWER_DAY,
                        precipitation_probability=38,
                        temp_celsius=13,
                        feels_like_temp_celsius=10,
                        wind_direction="S",
                        wind_speed_mph=13,
                        wind_gust_mph=25,
                        visibility="GO",
                        humidity_percent=85,
                        max_uv_index=1,
                    ),
                ),
                models.ForecastHour(
                    time=datetime.time(18, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.LIGHT_RAIN_SHOWER_DAY,
                        precipitation_probability=36,
                        temp_celsius=11,
                        feels_like_temp_celsius=9,
                        wind_direction="S",
                        wind_speed_mph=11,
                        wind_gust_mph=20,
                        visibility="MO",
                        humidity_percent=91,
                        max_uv_index=1,
                    ),
                ),
                models.ForecastHour(
                    time=datetime.time(21, 0),
                    weather=models.Weather(
                        weather_type=models.WeatherType.CLOUDY,
                        precipitation_probability=17,
                        temp_celsius=10,
                        feels_like_temp_celsius=8,
                        wind_direction="S",
                        wind_speed_mph=11,
                        wind_gust_mph=18,
                        visibility="GO",
                        humidity_percent=93,
                        max_uv_index=0,
                    ),
                ),
            ],
        ),
    ]

    assert actual == expected
