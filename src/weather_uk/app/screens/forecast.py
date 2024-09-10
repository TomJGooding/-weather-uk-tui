import requests
from textual.app import ComposeResult
from textual.containers import Horizontal, HorizontalScroll
from textual.screen import Screen
from textual.widgets import Footer, Tabs

from weather_uk.app.widgets.forecast_day import ForecastDayView
from weather_uk.app.widgets.forecast_labels import ForecastLabels
from weather_uk.data import models
from weather_uk.forecasts import services


class ForecastScreen(Screen):
    def compose(self) -> ComposeResult:
        forecast = self.get_forecast()

        yield Tabs(*[f"{day.date.strftime('%A')}" for day in forecast])

        with Horizontal():
            yield ForecastLabels()
            with HorizontalScroll():
                for day in forecast:
                    yield ForecastDayView(
                        day,
                        id=f"{day.date.strftime('%A')}",
                    )

        yield Footer()

    def on_mount(self) -> None:
        self.query_one(Tabs).focus()

    def get_forecast(self) -> list[models.ForecastDay]:
        weather_api = self.app._weather_api  # type: ignore[attr-defined]
        location_id = self.app._location_id  # type: ignore[attr-defined]
        forecast: list[models.ForecastDay] = []
        try:
            forecast = services.get_forecast(weather_api, location_id)
        # TODO: Handle requests exceptions
        except requests.exceptions.HTTPError:
            pass

        return forecast

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        day = str(event.tab.label)
        forecast_day = self.query_one(f"#{day}", ForecastDayView)
        self.query_one(HorizontalScroll).scroll_to_widget(forecast_day)
