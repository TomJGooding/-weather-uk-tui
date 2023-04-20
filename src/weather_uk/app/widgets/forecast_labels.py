from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import DataTable, Label


class ForecastLabels(Container):
    def compose(self) -> ComposeResult:
        yield Label(" ")
        yield DataTable(show_cursor=False, zebra_stripes=True)

    def on_mount(self) -> None:
        table = self.query_one(DataTable)

        weather_row: list[str] = ["[b]Weather type[/b]"]
        precip_chance_row: list[str] = ["[b]Chance of precip[/b]"]
        temp_row: list[str] = ["[b]Temperature (°C)[/b]"]
        feels_like_temp_row: list[str] = ["[b]Feels like temp (°C)[/b]"]
        wind_direction_row: list[str] = ["[b]Wind direction[/b]"]
        wind_speed_row: list[str] = ["[b]Wind speed (mph)[/b]"]
        wind_gust_row: list[str] = ["[b]Wind gust (mph)[/b]"]
        visibility_row: list[str] = ["[b]Visibility[/b]"]
        humidity_row: list[str] = ["[b]Humidity[/b]"]
        uv_row: list[str] = ["[b]UV[/b]"]

        table.add_column("")

        table_rows = [
            weather_row,
            precip_chance_row,
            temp_row,
            feels_like_temp_row,
            wind_direction_row,
            wind_speed_row,
            wind_gust_row,
            visibility_row,
            humidity_row,
            uv_row,
        ]
        for row in table_rows:
            table.add_row(*row)
