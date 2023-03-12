import requests
from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Footer, Input, Markdown
from textual_autocomplete import AutoComplete, Dropdown, DropdownItem

from weather_uk.adapters.weather_api import MetOfficeApi
from weather_uk.locations import services


class LocationsScreen(Screen):
    def on_mount(self) -> None:
        self.query_one(Input).focus()

    def compose(self) -> ComposeResult:
        yield Container(
            Markdown("# Find a forecast"),
            AutoComplete(
                Input(placeholder="Search for a location"),
                Dropdown(items=self.get_location_items()),
            ),
        )
        yield Footer()

    def get_location_items(self) -> list[DropdownItem]:
        api_key = self.app._api_key  # type: ignore[attr-defined]
        locations_data = []
        try:
            locations_data = services.get_locations_list(MetOfficeApi(api_key))
        except requests.exceptions.HTTPError:
            pass

        return [DropdownItem(str(location)) for location in locations_data]
