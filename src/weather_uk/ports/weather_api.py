from abc import ABC, abstractmethod

from weather_uk.data import models


class AbstractWeatherApi(ABC):
    @abstractmethod
    def check_authentication(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_locations_list(self) -> list[models.Location]:
        raise NotImplementedError

    @abstractmethod
    def get_forecast(self, location_id: int) -> list[models.ForecastDay]:
        raise NotImplementedError
