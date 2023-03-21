import datetime
from typing import Any

from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import DataTable, Label

from weather_uk.forecasts.models import ForecastDay, ForecastHour
from weather_uk.weather.model import Weather


class ForecastDayView(Container):
    def __init__(
        self,
        forecast_day: ForecastDay,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.date: datetime.date = forecast_day.date
        self.forecast_hours: list[ForecastHour] = forecast_day.hours

    def compose(self) -> ComposeResult:
        yield Label(self.date.strftime("%A"))
        yield DataTable(show_cursor=False, zebra_stripes=True)

    def on_mount(self) -> None:
        table = self.query_one(DataTable)

        weather_row: list[str] = ["Weather type"]
        precip_chance_row: list[str] = ["Chance of precip"]
        temp_row: list[str] = ["Temperature (°C)"]
        feels_like_temp_row: list[str] = ["Feels like temp (°C)"]
        wind_direction_row: list[str] = ["Wind direction"]
        wind_speed_row: list[str] = ["Wind speed (mph)"]
        wind_gust_row: list[str] = ["Wind gust (mph)"]
        visibility_row: list[str] = ["Visibility"]
        humidity_row: list[str] = ["Humidity"]
        uv_row: list[str] = ["UV"]

        table.add_column("")

        for hour in self.forecast_hours:
            table.add_column(hour.time.strftime("%H:%M"))

            weather: Weather = hour.weather
            weather_row.append(str(weather.weather_type))
            precip_chance_row.append(f"{weather.precipitation_probability}%")
            temp_row.append(f"{weather.temp_celsius}°")
            feels_like_temp_row.append(f"{weather.feels_like_temp_celsius}°")
            wind_direction_row.append(weather.wind_direction)
            wind_speed_row.append(f"{weather.wind_speed_mph}")
            wind_gust_row.append(f"{weather.wind_gust_mph}")
            visibility_row.append(weather.visibility)
            humidity_row.append(f"{weather.humidity_percent}%")
            uv_row.append(f"{weather.max_uv_index}")

        table_rows = [
            weather_row,
            precip_chance_row,
            temp_row,
            feels_like_temp_row,
            wind_direction_row,
            wind_speed_row,
            wind_gust_row,
            visibility_row,
            humidity_row,
            uv_row,
        ]
        for row in table_rows:
            table.add_row(*row)
