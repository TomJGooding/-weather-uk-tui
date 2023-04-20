import requests
from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Footer, Input, Label, Markdown

from weather_uk import config, ensure


class WelcomeScreen(Screen):
    def compose(self) -> ComposeResult:
        with Container(classes="center-box"):
            yield Markdown(WELCOME_MD)
            yield Label("Enter your API key:")
            yield Input(placeholder="Met Office DataPoint API key")
            yield Label(" ", id="auth-status")
            yield Markdown(DISCLAIMER_MD)
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        api_key = event.input.value.strip()
        weather_api = self.app._weather_api  # type: ignore[attr-defined]
        weather_api.api_key = api_key

        auth_msg = self.query_one("#auth-status", Label)
        try:
            ensure.valid_authentication(weather_api)
        except requests.exceptions.HTTPError as http_err:
            status_code = http_err.response.status_code
            if status_code == 403:
                auth_msg.styles.color = ERROR_COLOUR
                auth_msg.update(INVALID_KEY_MSG)

        # TODO: Handle other requests exceptions
        else:
            self.app._user_config = config.update_config(api_key)  # type: ignore[attr-defined]
            auth_msg.styles.color = SUCCESS_COLOUR
            auth_msg.update(SUCCESS_MSG)
            auth_msg.call_after_refresh(self.app.push_screen, "locations")


INVALID_KEY_MSG = "Error: Sorry, we couldn't validate your API key. Please try again."
SUCCESS_MSG = "Success! Loading..."

SUCCESS_COLOUR = "#4EBF71"
ERROR_COLOUR = "#ba3c5b"

DATAPOINT_URL: str = "https://www.metoffice.gov.uk/services/data/datapoint"

REGISTER_URL: str = (
    "https://register.metoffice.gov.uk/"
    "WaveRegistrationClient/public/newaccount.do"
    "?service=datapoint"
)

TERMS_URL: str = (
    "https://www.metoffice.gov.uk/services/data/datapoint/"
    "terms-and-conditions---datapoint"
)

FAIR_USE_URL: str = "https://www.metoffice.gov.uk/about-us/legal/fair-usage"

WELCOME_MD: str = f"""

# Welcome to weather-uk!

**weather-uk** is a terminal-based app to check UK weather forecasts,
using Met Office data from their freely available [DataPoint API]({DATAPOINT_URL}).

To use this app, you will need to [register with the Met Office]({REGISTER_URL})
to obtain an API key.

"""

DISCLAIMER_MD: str = f"""

---

*weather-uk has no association with the Met Office. By using this app you must
still comply with the Met Office's DataPoint
[Terms and conditions]({TERMS_URL}) and [Fair Use Policy]({FAIR_USE_URL}).*

"""
