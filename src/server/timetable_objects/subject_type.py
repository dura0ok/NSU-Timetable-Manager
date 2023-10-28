from dataclasses import dataclass
from typing import Optional

from .subject_type_color import SubjectTypeColor
from json_serializable import JSONSerializable


@dataclass(frozen=True)
class SubjectType(JSONSerializable):
    short_name: Optional[str]
    full_name: Optional[str]
    color: Optional[SubjectTypeColor]
    is_empty: bool = False


def create_empty_subject_type() -> SubjectType:
    return SubjectType(full_name=None, short_name=None, color=None, is_empty=True)
