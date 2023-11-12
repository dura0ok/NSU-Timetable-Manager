class ParsingException(Exception):
    pass


class TimetableParsingException(ParsingException):
    pass


class RoomParsingException(ParsingException):
    pass


class TutorNotFoundException(ParsingException):
    pass


class TutorParsingException(ParsingException):
    pass


class TimesParsingException(ParsingException):
    pass
