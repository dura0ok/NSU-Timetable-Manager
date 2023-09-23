from dataclasses import dataclass
from typing import List

import dataclass_wizard

from .subject import Subject


@dataclass(frozen=True)
class Cell(dataclass_wizard.JSONWizard):
    subjects: List[Subject]

    def is_empty(self) -> bool:
        return len(self.subjects) == 0


def empty_cell() -> Cell:
    return Cell([])
