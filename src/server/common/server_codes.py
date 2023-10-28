from enum import IntEnum, auto


class ServerCodes(IntEnum):
    def _generate_next_value_(self, start, count, last_values) -> int:
        return count

    SUCCESS = auto()
    INTERNAL_ERROR = auto()
    UNKNOWN_GROUP = auto()
    UNKNOWN_ROOM = auto()
    UNKNOWN_TUTOR = auto()
