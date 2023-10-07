from enum import IntEnum, auto


class ParsingCodes(IntEnum):
    def _generate_next_value_(self, start, count, last_values) -> int:
        return count

    SUCCESS = auto()
    INVALID_HTML = auto()
    UNKNOWN_ROOM = auto()
