import bs4

from server_codes import ServerCodes
from server_response import ServerResponse, create_error_parsing_result
from timetable_objects import Room, RoomLocation
from extraction.html_extraction.parsing.parsing_exceptions import RoomParsingException


class HTMLRoomParser:
    @staticmethod
    def parse_room(html_content: str) -> ServerResponse:
        try:
            room_name: str = HTMLRoomParser.__parse_room_name(html_content=html_content)
            room_location: RoomLocation = HTMLRoomParser.__parse_room_location(html_content=html_content)
            room: Room = Room(name=room_name, location=room_location)
        except RoomParsingException as e:
            return create_error_parsing_result(message=str(e), code=ServerCodes.INTERNAL_ERROR)

        return ServerResponse(result=room)

    @staticmethod
    def __parse_room_name(html_content: str) -> str:
        error_message: str = 'Invalid format of HTML: cannot parse room name'

        soup: bs4.BeautifulSoup = bs4.BeautifulSoup(html_content, features='html.parser')

        tag1: bs4.Tag = soup.find(name='div', attrs={'class': 'main_head'})
        if tag1 is None:
            raise RoomParsingException(error_message)

        tag2: bs4.Tag = tag1.find('h1')
        if tag2 is None:
            raise RoomParsingException(error_message)

        text: str = tag2.text
        if len(text) <= 10:
            raise RoomParsingException(error_message)

        return text[10:]

    @staticmethod
    def __parse_room_location(html_content: str) -> RoomLocation:
        error_message: str = 'Invalid format of HTML: cannot parse room location'

        i1 = html_content.find('room_view')
        if i1 == -1:
            raise RoomParsingException(error_message)

        i2 = html_content.find('(', i1)
        if i2 == -1:
            raise RoomParsingException(error_message)

        i3 = html_content.find(')', i1)
        if i3 == -1:
            raise RoomParsingException(error_message)

        values = html_content[i2 + 1:i3].split(',')

        try:
            block: str = values[0][6:-6]
            level: int = int(values[1])
            x: int = int(values[2])
            y: int = int(values[3])
        except IndexError as e:
            raise RoomParsingException(error_message) from e

        return RoomLocation(block=block, level=level, x=x, y=y)
