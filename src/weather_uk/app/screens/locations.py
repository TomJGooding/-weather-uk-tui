from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Footer, Input, Markdown

from weather_uk.app.widgets.locations import LocationSearch


class LocationsScreen(Screen):
    def compose(self) -> ComposeResult:
        with Container(classes="center-box"):
            yield Markdown("# Find a forecast")
            yield LocationSearch()
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(Input).focus()
