from textual.app import App

from weather_uk.adapters.weather_api import MetOfficeApi
from weather_uk.app.screens.locations import LocationsScreen
from weather_uk.app.screens.welcome import WelcomeScreen
from weather_uk.ports.weather_api import AbstractWeatherApi


class WeatherUkApp(App):
    CSS_PATH = "weather-uk.css"
    SCREENS = {
        "welcome": WelcomeScreen(),
        "locations": LocationsScreen(),
    }
    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
    ]

    def on_mount(self) -> None:
        self._weather_api: AbstractWeatherApi = MetOfficeApi()
        self.push_screen("welcome")


if __name__ == "__main__":
    app = WeatherUkApp()
    app.run()
