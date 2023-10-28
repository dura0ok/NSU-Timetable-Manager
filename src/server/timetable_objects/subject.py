from dataclasses import dataclass
from typing import Optional

from .periodicity import Periodicity
from .room import Room
from .subject_name import SubjectName
from .subject_type import SubjectType
from .tutor import Tutor
from json_serializable import JSONSerializable


@dataclass(frozen=True)
class Subject(JSONSerializable):
    name: Optional[SubjectName]
    type: Optional[SubjectType]
    tutor: Optional[Tutor]
    room: Optional[Room]
    periodicity: Optional[Periodicity]
    is_empty: bool = False


def create_empty_subject() -> Subject:
    return Subject(name=None, type=None, tutor=None, room=None, periodicity=None, is_empty=True)
