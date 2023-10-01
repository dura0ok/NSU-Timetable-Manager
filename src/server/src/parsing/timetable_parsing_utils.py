from typing import List, Optional, Mapping

import bs4

from src.timetable_objects import *
from .parsing_exceptions import TimetableParsingException


def parse_room_location(room_tag: Optional[bs4.element.Tag]) -> RoomLocation:
    error_message: str = 'Incorrect format of html: cannot parse room location'

    if room_tag is None:
        return empty_room_location()

    attr = room_tag.attrs.get('onclick')
    if attr is None or len(attr) <= 17:
        raise TimetableParsingException(error_message)

    try:
        onclick_arguments: List[str] = attr[17:-1].split(',')
        block: Optional[str] = onclick_arguments[0][1:-1]
        level: Optional[int] = int(onclick_arguments[1])
        x: Optional[int] = int(onclick_arguments[2])
        y: Optional[int] = int(onclick_arguments[3])
        return RoomLocation(block=block, level=level, x=x, y=y)
    except IndexError:
        raise TimetableParsingException(error_message)


def get_subject_type_color(subject_type: str) -> SubjectTypeColor:
    subject_type_color_map: Mapping['str', SubjectTypeColor] = {
        'lek': SubjectTypeColor.LECTURE,
        'pr': SubjectTypeColor.PRACTICAL,
        'lab': SubjectTypeColor.LAB,
        'f_2': SubjectTypeColor.ELECTIVE
    }

    ret: Optional[SubjectTypeColor] = subject_type_color_map.get(subject_type)

    if ret is None:
        raise TimetableParsingException(f'Incorrect format of html: unknown color of subject "{subject_type}"')

    return ret


def parse_tutor(subject_tag: bs4.element.Tag) -> Tutor:
    tag: bs4.element.Tag = subject_tag.find('a', {'class': 'tutor'})

    if tag is None:
        return empty_tutor()

    tutor_href: Optional[str] = tag.attrs.get('href')
    tutor_name: str = tag.text.strip()

    return Tutor(name=tutor_name, href=tutor_href)


def parse_room(subject_tag: bs4.element.Tag) -> Room:
    tag: bs4.element.Tag = subject_tag.find('div', {'class': 'room'})

    if tag is None:
        return empty_room()

    room_tag: bs4.element.Tag = tag.find('a')
    name: Optional[str] = tag.text.strip() if room_tag is None else room_tag.text.strip()
    location: RoomLocation = parse_room_location(room_tag=room_tag)

    return Room(name=name, location=location)


def parse_periodicity(subject_tag: bs4.element) -> Periodicity:
    week_tag: bs4.element.Tag = subject_tag.find('div', {'class': 'week'})

    if week_tag is None:
        return Periodicity.ON_ALL
    else:
        return Periodicity.ON_EVEN if week_tag.text.strip() == 'Четная' else Periodicity.ON_ODD


def parse_subject_name(subject_tag: bs4.element.Tag) -> SubjectName:
    name_tag: bs4.element.Tag = subject_tag.find('div', {'class': 'subject'})

    if name_tag is None:
        return empty_subject_name()

    short_name: str = name_tag.text.strip()
    full_name: str = name_tag.attrs.get('title')

    return SubjectName(full_name=full_name, short_name=short_name)


def parse_subject_type(subject_tag: bs4.element.Tag) -> SubjectType:
    type_tag: bs4.element.Tag = subject_tag.find('span')

    if type_tag is None:
        return empty_subject_type()

    short_name: str = type_tag.text.strip()
    full_name: str = type_tag.attrs.get('title')

    attr = type_tag.attrs.get('class')
    if attr is None or len(attr) < 2:
        raise TimetableParsingException('Incorrect format of html: cannot parse type of subject')

    color: SubjectTypeColor = get_subject_type_color(attr[1])

    return SubjectType(short_name=short_name, full_name=full_name, color=color)


def parse_subject(subject_tag: bs4.element.Tag) -> Subject:
    subject_name: SubjectName = parse_subject_name(subject_tag)
    subject_type: SubjectType = parse_subject_type(subject_tag)
    tutor: Tutor = parse_tutor(subject_tag)
    room: Room = parse_room(subject_tag)
    periodicity: Periodicity = parse_periodicity(subject_tag)

    return Subject(
        subject_name=subject_name,
        subject_type=subject_type,
        tutor=tutor,
        room=room,
        periodicity=periodicity,
    )


def parse_cell(cell_tag: bs4.element.Tag) -> Cell:
    subject_elements: bs4.ResultSet = cell_tag.find_all('div', {'class': 'cell'})

    subjects: List[Subject] = []
    for element in subject_elements:
        subjects.append(parse_subject(element))

    return Cell(subjects=subjects)
