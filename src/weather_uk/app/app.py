from textual.app import App, ComposeResult
from textual.widgets import Footer, Input

from weather_uk.app.widgets.welcome import Welcome


class WeatherUkApp(App):
    CSS_PATH = "weather-uk.css"
    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
    ]

    _api_key: str = ""

    def compose(self) -> ComposeResult:
        yield Welcome()
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#api-key", Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        api_key: str = event.input.value.strip()
        self._api_key = api_key
        self.query_one("#api-key", Input).value = ""


if __name__ == "__main__":
    app = WeatherUkApp()
    app.run()
