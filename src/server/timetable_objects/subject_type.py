from dataclasses import dataclass
from typing import Optional

from enum import IntEnum, auto

from serialization import JSONSerializable


class SubjectTypeColor(IntEnum):
    def _generate_next_value_(self, start, count, last_values) -> int:
        return count

    LECTURE = auto()
    PRACTICAL = auto()
    LAB = auto()
    ELECTIVE = auto()


@dataclass(frozen=True)
class SubjectType(JSONSerializable):
    short_name: Optional[str]
    full_name: Optional[str]
    color: Optional[SubjectTypeColor]
    is_empty: bool = False


def create_empty_subject_type() -> SubjectType:
    return SubjectType(full_name=None, short_name=None, color=None, is_empty=True)
