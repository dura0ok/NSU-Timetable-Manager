from dataclasses import dataclass
from typing import List

from .subject import Subject
from serialization import JSONSerializable


@dataclass(frozen=True)
class Cell(JSONSerializable):
    subjects: List[Subject]

    def is_empty(self) -> bool:
        return len(self.subjects) == 0


def create_empty_cell() -> Cell:
    return Cell([])
