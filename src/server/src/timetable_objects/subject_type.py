from dataclasses import dataclass
from typing import Optional

import strenum

from src.serialization.serializable import Serializable


class SubjectTypeColor(strenum.StrEnum):
    LECTURE = 'lek'
    PRACTICAL = 'pr'
    LAB = 'lab'
    ELECTIVE = 'f_2'


@dataclass(frozen=True)
class SubjectType(Serializable):
    short_name: Optional[str]
    full_name: Optional[str]
    color: Optional[SubjectTypeColor]
    is_empty: bool = False


def create_empty_subject_type() -> SubjectType:
    return SubjectType(full_name=None, short_name=None, color=None, is_empty=True)
