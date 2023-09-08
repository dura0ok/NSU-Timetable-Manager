from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Tuple, Optional

import dataclass_wizard


class Periodicity(IntEnum):
    def _generate_next_value_(self, start, count, last_values):
        return count

    ON_EVEN = auto()
    ON_ODD = auto()
    ON_ALL = auto()


@dataclass(frozen=True)
class Subject(dataclass_wizard.JSONWizard):
    name: Optional[str]
    teacher: Optional[str]
    place: Optional[str]
    periodicity: Optional[Periodicity]
    is_empty: bool


@dataclass(frozen=True)
class Day(dataclass_wizard.JSONWizard):
    name: str
    subjects: Tuple[Subject, ...]


@dataclass(frozen=True)
class Timetable(dataclass_wizard.JSONWizard):
    times: Tuple[str, ...]
    days: Tuple[Day, ...]
