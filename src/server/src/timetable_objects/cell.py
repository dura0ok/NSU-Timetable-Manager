from dataclasses import dataclass
from typing import List

from .subject import Subject
from src.serialization.serializable import Serializable


@dataclass(frozen=True)
class Cell(Serializable):
    subjects: List[Subject]

    def is_empty(self) -> bool:
        return len(self.subjects) == 0


def create_empty_cell() -> Cell:
    return Cell([])
