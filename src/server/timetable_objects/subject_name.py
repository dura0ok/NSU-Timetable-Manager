from dataclasses import dataclass
from typing import Optional

from serialization import JSONSerializable


@dataclass(frozen=True)
class SubjectName(JSONSerializable):
    full_name: Optional[str]
    short_name: Optional[str]
    is_empty: bool = False


def create_empty_subject_name() -> SubjectName:
    return SubjectName(full_name=None, short_name=None, is_empty=True)
