import datetime
from typing import Any

from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import DataTable, Label

from weather_uk.data import models


class ForecastDayView(Container):
    def __init__(
        self,
        forecast_day: models.ForecastDay,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.date: datetime.date = forecast_day.date
        self.forecast_hours: list[models.ForecastHour] = forecast_day.hours

    def compose(self) -> ComposeResult:
        yield Label(self.date.strftime("%A"))
        yield DataTable(show_cursor=False, zebra_stripes=True)

    def on_mount(self) -> None:
        table = self.query_one(DataTable)

        weather_row: list[str] = []
        precip_chance_row: list[str] = []
        temp_row: list[str] = []
        feels_like_temp_row: list[str] = []
        wind_direction_row: list[str] = []
        wind_speed_row: list[str] = []
        wind_gust_row: list[str] = []
        visibility_row: list[str] = []
        humidity_row: list[str] = []
        uv_row: list[str] = []

        for hour in self.forecast_hours:
            table.add_column(hour.time.strftime("%H:%M"))

            weather: models.Weather = hour.weather
            weather_row.append(str(weather.weather_type))
            precip_chance_row.append(
                self.colour_code_chance_of_precip(weather.precipitation_probability)
            )
            temp_row.append(f"{weather.temp_celsius}°")
            feels_like_temp_row.append(f"{weather.feels_like_temp_celsius}°")
            wind_direction_row.append(
                self.add_arrows(weather.wind_direction),
            )
            wind_speed_row.append(f"{weather.wind_speed_mph}")
            wind_gust_row.append(f"{weather.wind_gust_mph}")
            visibility_row.append(weather.visibility)
            humidity_row.append(f"{weather.humidity_percent}%")
            uv_row.append(
                self.colour_code_uv_index(weather.max_uv_index),
            )

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

    def colour_code_uv_index(self, uv_index: float) -> str:
        if uv_index > 10:
            return f"[white on purple3] {uv_index} [/white on purple3]"
        elif uv_index > 7:
            return f"[white on red3] {uv_index} [/white on red3]"
        elif uv_index > 5:
            return f"[black on dark_orange] {uv_index} [/black on dark_orange]"
        elif uv_index > 2:
            return f"[black on gold1] {uv_index} [/black on gold1]"
        elif uv_index > 0:
            return f"[black on green4] {uv_index} [/black on green4]"
        else:
            return f"[white on grey30] {uv_index} [/white on grey30]"

    def colour_code_chance_of_precip(self, chance_of_precip: float) -> str:
        if chance_of_precip >= 30:
            return (
                "[dark_blue on light_cyan1]"
                f"{chance_of_precip}%"
                "[/dark_blue on light_cyan1]"
            )
        else:
            return f"{chance_of_precip}%"

    def add_arrows(self, wind_direction: str) -> str:
        if wind_direction == "N":
            return f"↓ {wind_direction}"
        elif wind_direction == "E":
            return f"← {wind_direction}"
        elif wind_direction == "S":
            return f"↑ {wind_direction}"
        elif wind_direction == "W":
            return f"→ {wind_direction}"
        elif wind_direction[-2:] == "NE":
            return f"↙ {wind_direction}"
        elif wind_direction[-2:] == "NW":
            return f"↘ {wind_direction}"
        elif wind_direction[-2:] == "SE":
            return f"↖ {wind_direction}"
        elif wind_direction[-2:] == "SW":
            return f"↗ {wind_direction}"
        else:
            return wind_direction
