from enum import Enum


class ZeroEnum(Enum):
    """
    Class represents Enum that values start from zero.
    """

    def _generate_next_value_(self, start, count, last_values):
        return count
