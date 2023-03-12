from textual.app import App

from weather_uk.app.screens.locations import LocationsScreen
from weather_uk.app.screens.welcome import WelcomeScreen


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
        self._api_key: str = ""
        self.push_screen("welcome")


if __name__ == "__main__":
    app = WeatherUkApp()
    app.run()
