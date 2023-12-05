from typing import Optional

import bs4

from model.dto import Room, RoomLocation, create_empty_room_location
from .exceptions import RoomParsingException
from .utils import create_html_bs4


class HTMLRoomParser:
    __cannot_parse_room: str = 'Invalid format of HTML: cannot parse room'
    __cannot_parse_room_location: str = 'Invalid format of HTML: cannot parse room location'

    __room_tag_selector: str = 'div.main_head h1 a'
    __onclick_attr_name: str = 'onclick'

    @staticmethod
    def parse_room(html_content: str) -> Room:
        soup: bs4.BeautifulSoup = create_html_bs4(html_content)
        room_tag: bs4.Tag = HTMLRoomParser.__find_room_tag(soup)

        if room_tag is None:
            raise RoomParsingException(HTMLRoomParser.__cannot_parse_room)

        return HTMLRoomParser.parse_room_from_tag(room_tag=room_tag)

    @staticmethod
    def parse_room_from_tag(room_tag: bs4.Tag) -> Room:
        room_name: str = HTMLRoomParser.__parse_room_name(room_tag)
        room_location: RoomLocation = HTMLRoomParser.__parse_room_location(room_tag)
        return Room(name=room_name, location=room_location)

    @staticmethod
    def __find_room_tag(soup: bs4.BeautifulSoup) -> bs4.Tag:
        return soup.select_one(HTMLRoomParser.__room_tag_selector)

    @staticmethod
    def __parse_room_name(room_tag: bs4.Tag) -> str:
        return room_tag.text.strip()

    @staticmethod
    def __parse_room_location(room_tag: bs4.Tag) -> RoomLocation:
        on_click_attr: Optional[str] = room_tag.attrs.get(HTMLRoomParser.__onclick_attr_name)

        if on_click_attr is None:
            return create_empty_room_location()

        room_view_args: list[str] = HTMLRoomParser.__parse_first_function_args(on_click_attr)

        try:
            block: str = HTMLRoomParser.__remove_quotes(room_view_args[0])
            level: int = int(room_view_args[1])
            x: int = int(room_view_args[2])
            y: int = int(room_view_args[3])
        except IndexError as e:
            raise RoomParsingException(HTMLRoomParser.__cannot_parse_room_location) from e

        return RoomLocation(block=block, level=level, x=x, y=y)

    @staticmethod
    def __parse_first_function_args(html_content: str) -> list[str]:
        start: int = html_content.find('(')
        if start == -1:
            return []

        stop: int = html_content.find(')', start)
        if stop == -1:
            return []

        return html_content[start + 1:stop].split(',')

    @staticmethod
    def __remove_quotes(string: str) -> str:
        return string.replace('"', '').replace("'", "")
