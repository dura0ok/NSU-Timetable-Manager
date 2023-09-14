from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Optional

import dataclass_wizard


class SubjectTypeColor(IntEnum):
    def _generate_next_value_(self, start: int, count: int, last_values: list) -> int:
        return count

    LECTURE = auto()
    PRACTICAL = auto()
    LAB = auto()
    ELECTIVE = auto()


@dataclass(frozen=True)
class SubjectType(dataclass_wizard.JSONWizard):
    short_name: Optional[str]
    full_name: Optional[str]
    color: Optional[SubjectTypeColor]
    is_empty: bool = False


def empty_subject_type() -> SubjectType:
    return SubjectType(full_name=None, short_name=None, color=None, is_empty=True)
