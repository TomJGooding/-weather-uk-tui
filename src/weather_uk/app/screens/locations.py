from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Footer, Input, Markdown

from weather_uk.app.widgets.locations import LocationSearch


class LocationsScreen(Screen):
    def on_mount(self) -> None:
        self.query_one(Input).focus()

    def compose(self) -> ComposeResult:
        yield Container(
            Markdown("# Find a forecast"),
            LocationSearch(),
            classes=("center-box"),
        )
        yield Footer()
