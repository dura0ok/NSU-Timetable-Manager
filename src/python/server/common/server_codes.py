from enum import auto

from .zero_enum import ZeroEnum


class ServerCodes(ZeroEnum):
    SUCCESS = auto()
    INTERNAL_ERROR = auto()
    UNKNOWN_GROUP = auto()
    UNKNOWN_ROOM = auto()
    UNKNOWN_TUTOR = auto()
