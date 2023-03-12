import json
from pathlib import Path

import requests

from weather_uk.locations.model import Location
from weather_uk.ports.weather_api import AbstractWeatherApi

FAKE_DATA_DIR = Path(__file__).parent / "data"


class FakeMetOfficeApi(AbstractWeatherApi):
    BASE_URL: str = "http://datapoint.metoffice.gov.uk/public/data/"
    DATATYPE: str = "json"

    def __init__(self, api_key: str) -> None:
        self.api_key: str = api_key

    def _fake_request(self, resource: str) -> str:
        filename: str = resource
        return (FAKE_DATA_DIR / filename).read_text()

    def get_locations_list(self) -> list[Location]:
        resource: str = "sitelist"
        resp: str = self._fake_request(resource)

        result: list[Location] = []
        locations_data: list[dict] = json.loads(resp).get("Locations").get("Location")
        for location in locations_data:
            name: str | None = location.get("name")
            region: str | None = location.get("unitaryAuthArea")
            if name:
                result.append(Location(name, region))

        return result

    def _build_request(self, resource: str) -> requests.Request:
        url: str = f"{self.BASE_URL}{resource}?key={self.api_key}"
        return requests.Request(method="GET", url=url)


def test_build_request() -> None:
    api_key: str = "01234567-89ab-cdef-0123-456789abcdef"
    api = FakeMetOfficeApi(api_key)
    resource: str = "val/wxfcs/all/json/sitelist"

    assert api._build_request(resource).method == "GET"
    assert (
        api._build_request(resource).url
        == "http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/sitelist?key=01234567-89ab-cdef-0123-456789abcdef"
    )


def test_get_locations_list() -> None:
    api_key: str = "01234567-89ab-cdef-0123-456789abcdef"
    api = FakeMetOfficeApi(api_key)

    expected: list[str] = [
        "Carlisle Airport (Cumbria)",
        "Liverpool John Lennon Airport (Merseyside)",
        "Scatsta (Shetland Islands)",
        "Kinloss (Moray)",
        "Lossiemouth (Moray)",
        "Wick John O Groats Airport (Highland)",
        "Braemar (Aberdeenshire)",
        "Baltasound (Shetland Islands)",
        "Lerwick (S. Screen) (Shetland Islands)",
        "Fair Isle (Shetland Islands)",
    ]

    actual: list[str] = [str(location) for location in api.get_locations_list()]

    assert actual == expected
