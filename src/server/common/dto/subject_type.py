from enum import auto

from .zero_enum import ZeroEnum


class SubjectType(ZeroEnum):
    EMPTY = auto()
    LECTURE = auto()
    PRACTICAL = auto()
    LABORATORY = auto()
    LECTURE_ELECTIVE = auto()
    PRACTICAL_ELECTIVE = auto()
    LABORATORY_ELECTIVE = auto()
