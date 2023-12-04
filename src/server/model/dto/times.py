from dataclasses import dataclass


@dataclass(frozen=True)
class Times:
    times: list[str]
