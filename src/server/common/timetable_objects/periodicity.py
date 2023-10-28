from enum import IntEnum, auto


class Periodicity(IntEnum):
    def _generate_next_value_(self, start, count, last_values) -> int:
        return count

    ON_EVEN = auto()
    ON_ODD = auto()
    ON_ALL = auto()
