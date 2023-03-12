import json

import requests

from weather_uk.locations.model import Location
from weather_uk.ports.weather_api import AbstractWeatherApi


class MetOfficeApi(AbstractWeatherApi):
    BASE_URL: str = "http://datapoint.metoffice.gov.uk/public/data/"
    DATATYPE: str = "json"

    def __init__(self, api_key: str) -> None:
        self.api_key: str = api_key
        self._session: requests.Session = requests.Session()

    def get_locations_list(self) -> list[Location]:
        resource: str = f"val/wxfcs/all/{self.DATATYPE}/sitelist"
        resp: requests.Response = self._request(resource)

        result: list[Location] = []
        locations_data: list[dict] = (
            json.loads(resp.text).get("Locations").get("Location")
        )
        for location in locations_data:
            name: str | None = location.get("name")
            region: str | None = location.get("unitaryAuthArea")
            if name:
                result.append(Location(name, region))

        return result

    def _request(self, resource: str) -> requests.Response:
        req: requests.Request = self._build_request(resource)
        prepped: requests.PreparedRequest = req.prepare()
        try:
            resp: requests.Response = self._session.send(prepped)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            raise http_err
        except requests.exceptions.ConnectionError as cxn_err:
            raise cxn_err
        except requests.exceptions.Timeout as timeout_err:
            raise timeout_err
        except requests.exceptions.RequestException as req_err:
            raise req_err

        return resp

    def _build_request(self, resource: str) -> requests.Request:
        url: str = f"{self.BASE_URL}{resource}?key={self.api_key}"
        return requests.Request(method="GET", url=url)
