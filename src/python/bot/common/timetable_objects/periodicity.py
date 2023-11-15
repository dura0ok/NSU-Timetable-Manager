from enum import auto

from common.zero_enum import ZeroEnum


class Periodicity(ZeroEnum):
    ON_EVEN = auto()
    ON_ODD = auto()
    ON_ALL = auto()
