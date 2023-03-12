import dataclasses


@dataclasses.dataclass
class Location:
    name: str
    region: str | None

    def __str__(self) -> str:
        if self.region:
            return f"{self.name} ({self.region})"
        else:
            return self.name
