import requests
from textual.app import ComposeResult
from textual.widgets import Input, Static
from textual_autocomplete import AutoComplete, Dropdown, DropdownItem

from weather_uk.domain.locations import get_locations_list


class LocationSearch(Static):
    def compose(self) -> ComposeResult:
        yield AutoComplete(
            Input(placeholder="Search for a location"),
            Dropdown(items=self.get_location_items()),
        )

    def on_mount(self) -> None:
        self.query_one(Input).focus()

    def get_location_items(self) -> list[DropdownItem]:
        weather_api = self.app._weather_api  # type: ignore[attr-defined]
        locations_data = []
        try:
            locations_data = get_locations_list(weather_api)

        # TODO: Handle requests exceptions
        except requests.exceptions.HTTPError:
            pass

        return [
            DropdownItem(main=str(location), right_meta=str(location.id))
            for location in locations_data
        ]

    def on_auto_complete_selected(self, event: AutoComplete.Selected) -> None:
        location_id: int = int(str(event.item.right_meta))
        self.app._location_id = location_id  # type: ignore[attr-defined]
        self.app.push_screen("forecast")
