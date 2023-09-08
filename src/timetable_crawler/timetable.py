import json
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Tuple, Optional

import dataclass_wizard


class Periodicity(IntEnum):
    def _generate_next_value_(self, start, count, last_values) -> int:
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


if __name__ == "__main__":
    import random


    # Generate random data for the Timetable object
    def generate_random_subject():
        name = random.choice(['Math', 'Science', 'English'])
        teacher = random.choice(['Mr. Smith', 'Mrs. Johnson', 'Ms. Thompson'])
        place = random.choice(['Room 101', 'Room 202', 'Room 303'])
        periodicity = random.choice(list(Periodicity))
        is_empty = bool(random.getrandbits(1))
        return Subject(name=name, teacher=teacher, place=place, periodicity=periodicity, is_empty=is_empty)


    times = ('9:00', '10:00', '11:00')
    days = (
        Day('Monday', tuple([generate_random_subject() for i in range(10)])),
    )

    t = Timetable(times, days)
    print(t.to_json())
