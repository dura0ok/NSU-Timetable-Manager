from enum import IntEnum, auto


class SubjectTypeColor(IntEnum):
    def _generate_next_value_(self, start, count, last_values) -> int:
        return count

    LECTURE = auto()
    PRACTICAL = auto()
    LAB = auto()
    ELECTIVE = auto()
