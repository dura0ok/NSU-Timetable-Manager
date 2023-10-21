from dataclasses import dataclass
from typing import Optional

from .periodicity import Periodicity
from .room import Room
from .subject_name import SubjectName
from .subject_type import SubjectType
from serialization import JSONSerializable
from .tutor import Tutor


@dataclass(frozen=True)
class Subject(JSONSerializable):
    subject_name: Optional[SubjectName]
    subject_type: Optional[SubjectType]
    tutor: Optional[Tutor]
    room: Optional[Room]
    periodicity: Optional[Periodicity]
    is_empty: bool = False


def create_empty_subject() -> Subject:
    return Subject(subject_name=None, subject_type=None, tutor=None, room=None, periodicity=None, is_empty=True)
