from src.timetable_objects import Tutor
from .parsing_exceptions import TutorParsingException, ParsingException
from .tutor_parsing_utils import extract_tutor_href, parse_tutor_name_from_single_tutor_page, download_tutors_page, \
    parse_tutor_href_by_short_name, parse_tutor_name_by_short_name, parse_tutor_href_by_full_name, \
    parse_tutor_name_by_full_name
from .utils import HTMLDownloadingException, download_html


def parse_tutor_from_url(url: str) -> Tutor:
    """
    Parses object of :class:`src.timetable_objects.Tutor` from url.

    Examples of valid urls

    https://table.nsu.ru/teacher/fa7901fc-0846-11e6-8153-000c29b4927a

    https://table.nsu.ru/teacher/854d29c3-d630-11ea-80f9-0050568bc8ee

    :param url: url of tutor.
    """

    try:
        href: str = extract_tutor_href(url)
        content = download_html(url)
        name: str = parse_tutor_name_from_single_tutor_page(content)
        return Tutor(name=name, href=href)
    except HTMLDownloadingException:
        raise TutorParsingException(f'Tutor not found on url {url}')


def parse_tutor_by_short_name(short_name: str) -> Tutor:
    """
    Parses object of :class:`src.timetable_objects.Tutor` by short name. It can contain any number of spaces at the
    beginning and at the end. Format: "<last name> <shortened first name>.<shortened patronymic>.".

    Examples of valid short names

    Доманова Е.Д.
    Валишев А.И.

    :param short_name: short name of tutor in appropriate format.
    """

    content: str = download_tutors_page()

    striped_short_name = short_name.strip()
    if content.find(striped_short_name) == -1:
        raise ParsingException(f'Unknown tutor with short name "{striped_short_name}"')

    href: str = parse_tutor_href_by_short_name(html_page=content, short_name=striped_short_name)
    name: str = parse_tutor_name_by_short_name(html_page=content, short_name=striped_short_name)

    return Tutor(name=name, href=href)


def parse_tutor_by_full_name(full_name: str) -> Tutor:
    """
    Parses object of :class:`src.timetable_objects.Tutor` by full name. It can contain any number of spaces at the
    beginning and at the end. Format: "<last name> <first name> <patronymic>".

    Examples of valid full names

    Доманова Елена Дмитриевна
    Валишев Абрик Ибрагимович

    :param full_name: full name of tutor in appropriate format.
    """

    content: str = download_tutors_page()

    striped_full_name = full_name.strip()

    if content.find(striped_full_name) == -1:
        raise ParsingException(f'Unknown tutor with full name "{striped_full_name}"')

    href: str = parse_tutor_href_by_full_name(html_page=content, full_name=striped_full_name)
    name: str = parse_tutor_name_by_full_name(html_page=content, full_name=striped_full_name)

    return Tutor(name=name, href=href)
