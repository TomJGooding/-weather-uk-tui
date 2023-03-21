from __future__ import annotations

import datetime
from dataclasses import dataclass

from weather_uk.weather.model import Weather


@dataclass(order=True)
class ForecastDay:
    date: datetime.date
    hours: list[ForecastHour]


@dataclass()
class ForecastHour:
    time: datetime.time
    weather: Weather
