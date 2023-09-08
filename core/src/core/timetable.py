from dataclasses import dataclass
from enum import IntEnum
from typing import Tuple, Optional

import dataclass_wizard


class Periodicity(IntEnum):
    on_even = 0,
    on_odd = 1,
    on_all = 2


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
