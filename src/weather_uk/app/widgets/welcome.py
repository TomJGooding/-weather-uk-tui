from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Input, Label, Markdown


class Welcome(Container):
    def compose(self) -> ComposeResult:
        yield Markdown(WELCOME_MD)
        yield Label("[b]Enter your API key:[/b]")
        yield Input(
            placeholder="Met Office DataPoint API key",
            id="api-key",
        )
        yield Markdown(DISCLAIMER_MD)


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

**weather-uk** is a terminal-based app to check UK weather forecasts, using Met
Office data from their freely available [DataPoint API]({DATAPOINT_URL}).

To use this app, you will need to
[register with the Met Office]({REGISTER_URL}) to obtain an API key.

"""

DISCLAIMER_MD: str = f"""

---

*weather-uk has no association with the Met Office. By using this app you must
still comply with the Met Office's DataPoint
[Terms and conditions]({TERMS_URL}) and [Fair Use Policy]({FAIR_USE_URL}).*

"""
