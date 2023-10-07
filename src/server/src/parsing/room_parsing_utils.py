import bs4

from src.timetable_objects import Room, RoomLocation
from .parsing_exceptions import RoomParsingException


def get_room_url(room_name: str) -> str:
    url_name: str = ' '.join(room_name.split()).replace(' ', '+')
    return f'https://table.nsu.ru/room/{url_name}'


def parse_room_name(html_page: str) -> str:
    error_message: str = 'Invalid format of HTML: cannot parse room name'

    soup: bs4.BeautifulSoup = bs4.BeautifulSoup(html_page, 'html.parser')

    tag1: bs4.Tag = soup.find('div', {'class': 'main_head'})
    if tag1 is None:
        raise RoomParsingException(error_message)

    tag2: bs4.Tag = tag1.find('h1')
    if tag2 is None:
        raise RoomParsingException(error_message)

    text: str = tag2.text
    if len(text) <= 10:
        raise RoomParsingException(error_message)

    return text[10:]


def parse_room_location(html_page: str) -> RoomLocation:
    error_message: str = 'Invalid format of HTML: cannot parse room location'

    i1 = html_page.find('room_view')
    if i1 == -1:
        raise RoomParsingException(error_message)

    i2 = html_page.find('(', i1)
    if i2 == -1:
        raise RoomParsingException(error_message)

    i3 = html_page.find(')', i1)
    if i3 == -1:
        raise RoomParsingException(error_message)

    values = html_page[i2 + 1:i3].split(',')

    try:
        block: str = values[0][6:-6]
        level: int = int(values[1])
        x: int = int(values[2])
        y: int = int(values[3])
        return RoomLocation(block=block, level=level, x=x, y=y)
    except IndexError as e:
        raise RoomParsingException(error_message) from e


def parse_room_from_html(html_page: str) -> Room:
    room_name: str = parse_room_name(html_page)
    if room_name.isspace():
        raise RoomParsingException('Invalid format of HTML: parsed room name cannot be empty')

    room_location: RoomLocation = parse_room_location(html_page)

    return Room(name=room_name, location=room_location)
