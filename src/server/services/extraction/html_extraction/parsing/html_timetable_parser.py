from typing import Optional

import bs4

from model.dto import SubjectType, Periodicity, Timetable, Times, Cell, Subject, SubjectName, Tutor, Room, \
    create_empty_tutor, create_empty_room
from .html_times_parser import HTMLTimesParser
from .html_room_parser import HTMLRoomParser
from .html_tutor_parser import HTMLTutorParser
from .parsing_exceptions import TimetableParsingException, RoomParsingException, TutorParsingException
from .utils import create_html_bs4


class HTMLTimetableParser:
    __timetable_line_selector: str = 'table.time-table tr'
    __subject_selector: str = 'div.cell'
    __subject_name_selector: str = 'div.subject'
    __tutor_selector: str = 'a.tutor'
    __room_selector: str = 'div.room'
    __week_selector: str = 'div.week'
    __cell_tag_name: str = 'td'
    __subject_type_tag_name: str = 'span'
    __full_subject_name_attr_name: str = 'title'

    __no_timetable_found: str = 'Invalid format of HTML: cannot find timetable'
    __no_cells_in_row: str = 'Invalid format of HTML: no cells in timetable-row'
    __subject_without_name_tag: str = 'Invalid format of HTML: found subject without name-tag'
    __subject_without_full_name: str = 'Invalid format of HTML: found subject without full name'
    __subject_without_type: str = 'Invalid format of HTML: found subject without type'
    __cannot_parse_tutor: str = 'Invalid format of HTML: cannot parse tutor of subject'
    __cannot_parse_room: str = 'Invalid format of HTML: cannot parse room of subject'

    __subject_type_map: dict[str, SubjectType] = {
        'лек': SubjectType.LECTURE,
        'пр': SubjectType.PRACTICAL,
        'лаб': SubjectType.LECTURE,
        'ф, лек': SubjectType.LECTURE_ELECTIVE,
        'ф, пр': SubjectType.PRACTICAL_ELECTIVE,
        'ф, лаб': SubjectType.LABORATORY_ELECTIVE
    }

    __periodicity_map: dict[str, Periodicity] = {
        'Четная': Periodicity.ON_EVEN,
        'Нечетная': Periodicity.ON_ODD,
    }

    @staticmethod
    def parse_timetable(html_content: str) -> Timetable:
        soup: bs4.BeautifulSoup = create_html_bs4(html_content)

        times: Times = HTMLTimesParser.parse_times(html_content)
        cells: list[Cell] = HTMLTimetableParser.__parse_cells(soup=soup)

        return Timetable(cells=cells, times=times)

    @staticmethod
    def __parse_cells(soup: bs4.BeautifulSoup) -> list[Cell]:
        rows: bs4.ResultSet = soup.select(HTMLTimetableParser.__timetable_line_selector)
        if len(rows) == 0:
            raise TimetableParsingException(HTMLTimetableParser.__no_timetable_found)

        cells: list[Cell] = []

        # We have to skip first row, because it contains only days of week
        for row in rows[1:]:
            cells_tags: bs4.ResultSet = row.find_all(HTMLTimetableParser.__cell_tag_name)

            if len(cells_tags) == 0:
                raise TimetableParsingException(HTMLTimetableParser.__no_cells_in_row)

            # We have to skip first cell-tag because it contains only time
            for tag in cells_tags[1:]:
                cells.append(HTMLTimetableParser.__parse_cell(tag))

        return cells

    @staticmethod
    def __parse_cell(cell_tag: bs4.Tag) -> Cell:
        subjects_tags: bs4.ResultSet = cell_tag.select(HTMLTimetableParser.__subject_selector)
        subjects: list[Subject] = []

        for tag in subjects_tags:
            subject: Subject = HTMLTimetableParser.__parse_subject(tag)
            subjects.append(subject)

        return Cell(subjects)

    @staticmethod
    def __parse_subject(subject_tag: bs4.Tag) -> Subject:
        subject_name: SubjectName = HTMLTimetableParser.__parse_subject_name(subject_tag)
        subject_type: SubjectType = HTMLTimetableParser.__parse_subject_type(subject_tag)
        tutor: Tutor = HTMLTimetableParser.__parse_tutor(subject_tag)
        room: Room = HTMLTimetableParser.__parse_room(subject_tag)
        periodicity: Periodicity = HTMLTimetableParser.__parse_periodicity(subject_tag)

        return Subject(
            name=subject_name,
            type=subject_type,
            tutor=tutor,
            room=room,
            periodicity=periodicity,
        )

    @staticmethod
    def __parse_subject_name(subject_tag: bs4.Tag) -> SubjectName:
        name_tag: bs4.Tag = subject_tag.select_one(HTMLTimetableParser.__subject_name_selector)

        if name_tag is None:
            raise TimetableParsingException(HTMLTimetableParser.__subject_without_name_tag)

        short_name: str = name_tag.text.strip()
        full_name: Optional[str] = name_tag.attrs.get(HTMLTimetableParser.__full_subject_name_attr_name)

        if full_name is None:
            raise TimetableParsingException(HTMLTimetableParser.__subject_without_full_name)

        return SubjectName(full_name=full_name, short_name=short_name)

    @staticmethod
    def __parse_subject_type(subject_tag: bs4.Tag) -> SubjectType:
        type_tag: bs4.Tag = subject_tag.find(HTMLTimetableParser.__subject_type_tag_name)
        if type_tag is None:
            raise TimetableParsingException(HTMLTimetableParser.__subject_without_type)

        type_name: str = type_tag.text.strip()
        if type_name not in HTMLTimetableParser.__subject_type_map.keys():
            raise TimetableParsingException(HTMLTimetableParser.__get_unknown_subject_type_message(type_name))

        return HTMLTimetableParser.__subject_type_map.get(type_name)

    @staticmethod
    def __parse_tutor(subject_tag: bs4.Tag) -> Tutor:
        tutor_tag: bs4.Tag = subject_tag.select_one(HTMLTimetableParser.__tutor_selector)

        if tutor_tag is None:
            return create_empty_tutor()

        try:
            tutor: Tutor = HTMLTutorParser.parse_tutor_from_tag(tutor_tag)
        except TutorParsingException as e:
            raise TimetableParsingException(HTMLTimetableParser.__cannot_parse_tutor) from e

        return tutor

    @staticmethod
    def __parse_room(subject_tag: bs4.Tag) -> Room:
        room_tag: bs4.Tag = subject_tag.select_one(HTMLTimetableParser.__room_selector)

        if room_tag is None:
            return create_empty_room()

        try:
            room: Room = HTMLRoomParser.parse_room_from_tag(room_tag)
        except RoomParsingException as e:
            raise TimetableParsingException(HTMLTimetableParser.__cannot_parse_room) from e

        return room

    @staticmethod
    def __parse_periodicity(subject_tag: bs4.Tag) -> Periodicity:
        week_tag: bs4.Tag = subject_tag.select_one(HTMLTimetableParser.__week_selector)

        if week_tag is None:
            return Periodicity.ON_ALL

        periodicity_name: str = week_tag.text.strip()

        # Unknown periodicity
        if HTMLTimetableParser.__periodicity_map.get(periodicity_name) is None:
            raise TimetableParsingException(HTMLTimetableParser.__get_unknown_periodicity_message(periodicity_name))

        return HTMLTimetableParser.__periodicity_map.get(periodicity_name)

    @staticmethod
    def __get_unknown_subject_type_message(subject_type: str) -> str:
        return f'Invalid format of HTML: found unknown subject type "{subject_type}"'

    @staticmethod
    def __get_unknown_periodicity_message(periodicity: str) -> str:
        return f'Invalid format of HTML: found unknown periodicity "{periodicity}"'
