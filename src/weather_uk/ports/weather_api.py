from abc import ABC, abstractmethod

from weather_uk.locations.model import Location


class AbstractWeatherApi(ABC):
    @abstractmethod
    def get_locations_list(self) -> list[Location]:
        raise NotImplementedError
