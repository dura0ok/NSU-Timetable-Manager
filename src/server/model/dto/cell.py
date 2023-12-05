from dataclasses import dataclass

from .subject import Subject


@dataclass(frozen=True)
class Cell:
    subjects: list[Subject]
