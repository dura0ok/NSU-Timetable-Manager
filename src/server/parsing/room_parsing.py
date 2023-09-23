import requests
from requests import Response

from src.timetable_objects import Room, empty_room_location
from .room_parsing_utils import get_room_url, parse_room_from_html


def parse_room(room_name: str) -> Room:
    """
    Parses object of :class:`src.timetable_objects.Room` using name of room.
    Name of room can contain any number of spaces (>0) between words, at the beginning and at the end.
    Case doesn't matter for valid room-names. If name is invalid then function will return object of
    :class:`src.timetable_objects.Room`, but field `location` will be empty and name will be equal `room_name`
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

    response: Response = requests.get(get_room_url(room_name))

    if response.status_code != 200:
        return Room(name=room_name, location=empty_room_location())

    return parse_room_from_html(response.text)
