import requests
from textual.app import ComposeResult
from textual.containers import Horizontal, HorizontalScroll
from textual.screen import Screen
from textual.widgets import Footer

from weather_uk.app.widgets.forecast_day import ForecastDayView
from weather_uk.app.widgets.forecast_labels import ForecastLabels
from weather_uk.forecasts import services
from weather_uk.forecasts.models import ForecastDay


class ForecastScreen(Screen):
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield ForecastLabels()
            with HorizontalScroll():
                for day in self.get_forecast():
                    yield ForecastDayView(day)
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(HorizontalScroll).focus()

    def get_forecast(self) -> list[ForecastDay]:
        weather_api = self.app._weather_api  # type: ignore[attr-defined]
        location_id = self.app._location_id  # type: ignore[attr-defined]
        forecast: list[ForecastDay] = []
        try:
            forecast = services.get_forecast(weather_api, location_id)
        # TODO: Handle requests exceptions
        except requests.exceptions.HTTPError:
            pass

        return forecast
