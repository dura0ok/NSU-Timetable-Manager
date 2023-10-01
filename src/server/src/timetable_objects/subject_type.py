from dataclasses import dataclass
from typing import Optional

import dataclass_wizard
import strenum


class SubjectTypeColor(strenum.StrEnum):
    LECTURE = 'lek'
    PRACTICAL = 'pr'
    LAB = 'lab'
    ELECTIVE = 'f_2'


@dataclass(frozen=True)
class SubjectType(dataclass_wizard.JSONWizard):
    short_name: Optional[str]
    full_name: Optional[str]
    color: Optional[SubjectTypeColor]
    is_empty: bool = False


def empty_subject_type() -> SubjectType:
    return SubjectType(full_name=None, short_name=None, color=None, is_empty=True)
