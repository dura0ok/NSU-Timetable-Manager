from src.timetable_objects import Room
from .room_parsing_utils import get_room_url, parse_room_from_html
from .parsing_exceptions import RoomParsingException
from .utils import download_html, HTMLDownloadingException


def parse_room(room_name: str) -> Room:
    """
    Parses object of :class:`src.timetable_objects.Room` using name of room.
    Name of room can contain any positive number of spaces between words, at the beginning and at the end, case
    doesn't matter.

    Examples of valid names:

    3107

    402 ГК

    433 ЛК

    118а ЛК

    т2221

    т212 ГК

    т531 ЛК

    МА

    БА

    1216 студия

    :param room_name: name of room.
    """

    if room_name.isspace():
        raise RoomParsingException('Room name cannot be whitespace-string')

    striped_room_name = room_name.strip()

    try:
        content: str = download_html(get_room_url(striped_room_name))
        return parse_room_from_html(content)
    except HTMLDownloadingException:
        raise RoomParsingException(f'Room with name "{striped_room_name}" not found')
