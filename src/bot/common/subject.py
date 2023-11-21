from dataclasses import dataclass

from .periodicity import Periodicity
from .room import Room
from .subject_name import SubjectName
from .subject_type import SubjectType
from .tutor import Tutor


@dataclass(frozen=True)
class Subject:
    name: SubjectName
    type: SubjectType
    tutor: Tutor
    room: Room
    periodicity: Periodicity
