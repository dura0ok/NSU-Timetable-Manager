from enum import auto

from ..utils import ZeroEnum


class Periodicity(ZeroEnum):
    ON_EVEN = auto()
    ON_ODD = auto()
    ON_ALL = auto()
