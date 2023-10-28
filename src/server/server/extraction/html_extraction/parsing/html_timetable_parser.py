from typing import List, Optional, Mapping

import bs4

from common.server_codes import ServerCodes
from common.server_response import ServerResponse, create_error_parsing_result
from common.timetable_objects import *
from server.extraction.html_extraction.parsing.parsing_exceptions import TimetableParsingException


class HTMLTimetableParser:
    @staticmethod
    def parse_timetable(html_content: str) -> ServerResponse:
        try:
            soup: bs4.BeautifulSoup = bs4.BeautifulSoup(markup=html_content, features='html.parser')
            timetable: Timetable = HTMLTimetableParser.__parse_timetable(soup=soup)
        except TimetableParsingException as e:
            return create_error_parsing_result(message=str(e), code=ServerCodes.INTERNAL_ERROR)

        return ServerResponse(timetable)

    @staticmethod
    def __parse_timetable(soup: bs4.BeautifulSoup) -> Timetable:
        timetable_tag: bs4.Tag = soup.find(name='table', attrs={'class': 'time-table'})

        if timetable_tag is None:
            raise TimetableParsingException('Invalid format of HTML: timetable not found on the page')

        trs: bs4.ResultSet = timetable_tag.find_all('tr')
        if len(trs) == 0:
            raise TimetableParsingException('Invalid format of HTML: invalid format of timetable')

        cells: List[Cell] = []
        times: List[str] = []

        #  Parsing of times and cells
        for tr in trs[1:]:
            tds: bs4.ResultSet = tr.find_all('td')

            if len(tds) != 7:
                raise TimetableParsingException('Invalid format of HTML: invalid number of columns in timetable')

            time: str = tds[0].text.strip()
            times.append(time)

            for td in tds[1:]:
                cells.append(HTMLTimetableParser.__parse_cell(cell_tag=td))

        return Timetable(cells=cells, times=times)

    @staticmethod
    def __parse_cell(cell_tag: bs4.element.Tag) -> Cell:
        subject_elements: bs4.ResultSet = cell_tag.find_all(name='div', attrs={'class': 'cell'})

        subjects: List[Subject] = []
        for element in subject_elements:
            subjects.append(HTMLTimetableParser.__parse_subject(subject_tag=element))

        return Cell(subjects=subjects)

    @staticmethod
    def __parse_subject(subject_tag: bs4.element.Tag) -> Subject:
        subject_name: SubjectName = HTMLTimetableParser.__parse_subject_name(subject_tag=subject_tag)
        subject_type: SubjectType = HTMLTimetableParser.__parse_subject_type(subject_tag=subject_tag)
        tutor: Tutor = HTMLTimetableParser.__parse_tutor(subject_tag=subject_tag)
        room: Room = HTMLTimetableParser.__parse_room(subject_tag=subject_tag)
        periodicity: Periodicity = HTMLTimetableParser.__parse_periodicity(subject_tag=subject_tag)

        return Subject(
            name=subject_name,
            type=subject_type,
            tutor=tutor,
            room=room,
            periodicity=periodicity,
        )

    @staticmethod
    def __parse_subject_name(subject_tag: bs4.element.Tag) -> SubjectName:
        name_tag: bs4.element.Tag = subject_tag.find(name='div', attrs={'class': 'subject'})

        if name_tag is None:
            return create_empty_subject_name()

        short_name: str = name_tag.text.strip()
        full_name: str = name_tag.attrs.get('title')

        return SubjectName(full_name=full_name, short_name=short_name)

    @staticmethod
    def __parse_subject_type(subject_tag: bs4.element.Tag) -> SubjectType:
        type_tag: bs4.element.Tag = subject_tag.find(name='span')

        if type_tag is None:
            return create_empty_subject_type()

        short_name: str = type_tag.text.strip()
        full_name: str = type_tag.attrs.get('title')

        attr = type_tag.attrs.get('class')
        if attr is None or len(attr) < 2:
            raise TimetableParsingException('Invalid format of HTML: cannot parse type of subject')

        color: SubjectTypeColor = HTMLTimetableParser.__extract_subject_type_color(subject_type=attr[1])

        return SubjectType(short_name=short_name, full_name=full_name, color=color)

    @staticmethod
    def __parse_tutor(subject_tag: bs4.element.Tag) -> Tutor:
        tag: bs4.element.Tag = subject_tag.find(name='a', attrs={'class': 'tutor'})

        if tag is None:
            return empty_tutor()

        tutor_href: Optional[str] = tag.attrs.get('href')
        tutor_name: str = tag.text.strip()

        return Tutor(name=tutor_name, href=tutor_href)

    @staticmethod
    def __parse_room(subject_tag: bs4.element.Tag) -> Room:
        tag: bs4.element.Tag = subject_tag.find(name='div', attrs={'class': 'room'})

        if tag is None:
            return create_empty_room()

        room_tag: bs4.element.Tag = tag.find('a')
        name: Optional[str] = tag.text.strip() if room_tag is None else room_tag.text.strip()
        location: RoomLocation = HTMLTimetableParser.__parse_room_location(room_tag=room_tag)

        return Room(name=name, location=location)

    @staticmethod
    def __parse_periodicity(subject_tag: bs4.element) -> Periodicity:
        week_tag: bs4.element.Tag = subject_tag.find(name='div', attrs={'class': 'week'})

        if week_tag is None:
            return Periodicity.ON_ALL
        else:
            return Periodicity.ON_EVEN if week_tag.text.strip() == 'Четная' else Periodicity.ON_ODD

    @staticmethod
    def __extract_subject_type_color(subject_type: str) -> SubjectTypeColor:
        subject_type_color_map: Mapping['str', SubjectTypeColor] = {
            'lek': SubjectTypeColor.LECTURE,
            'pr': SubjectTypeColor.PRACTICAL,
            'lab': SubjectTypeColor.LAB,
            'f_2': SubjectTypeColor.ELECTIVE
        }

        ret: Optional[SubjectTypeColor] = subject_type_color_map.get(subject_type)

        if ret is None:
            raise TimetableParsingException(f'Invalid format of HTML: unknown color of subject {subject_type}')

        return ret

    @staticmethod
    def __parse_room_location(room_tag: Optional[bs4.element.Tag]) -> RoomLocation:
        error_message: str = 'Invalid format of HTML: cannot parse location of room of subject'

        if room_tag is None:
            return create_empty_room_location()

        attr: str = room_tag.attrs.get('onclick')
        if attr is None or len(attr) <= 17:
            raise TimetableParsingException(error_message)

        try:
            onclick_arguments: List[str] = attr[17:-1].split(',')
            block: Optional[str] = onclick_arguments[0][1:-1]
            level: Optional[int] = int(onclick_arguments[1])
            x: Optional[int] = int(onclick_arguments[2])
            y: Optional[int] = int(onclick_arguments[3])
        except IndexError as e:
            raise TimetableParsingException(error_message) from e

        return RoomLocation(block=block, level=level, x=x, y=y)
