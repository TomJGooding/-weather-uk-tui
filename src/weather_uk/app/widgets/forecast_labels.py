from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import DataTable, Label


class ForecastLabels(Container):
    def compose(self) -> ComposeResult:
        yield Label(" ")
        yield DataTable(show_cursor=False, zebra_stripes=True)

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        labels = (
            "Weather type",
            "Chance of precip",
            "Temperature (°C)",
            "Feels like temp (°C)",
            "Wind direction",
            "Wind speed (mph)",
            "Wind gust (mph)",
            "Visibility",
            "Humidity",
            "UV",
        )
        table.add_column("")
        for label in labels:
            table.add_row(label)
