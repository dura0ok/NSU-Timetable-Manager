from typing import List

import bs4

from src.timetable_objects import Timetable, Cell
from .parsing_exceptions import TimetableParsingException
from .timetable_parsing_utils import parse_cell
from .utils import HTMLDownloadingException, download_html


def parse_timetable_from_html(html_page: str) -> Timetable:
    """
    Parses object of :class:`src.timetable_objects.Timetable` using html-page of timetable.

    :param html_page: string with html-page of timetable.
    """

    soup: bs4.BeautifulSoup = bs4.BeautifulSoup(html_page, 'html.parser')
    timetable_tag: bs4.Tag = soup.find('table', {'class': 'time-table'})

    if timetable_tag is None:
        raise TimetableParsingException("Incorrect format of html: timetable not found")

    trs: bs4.ResultSet = timetable_tag.find_all('tr')
    if len(trs) == 0:
        raise TimetableParsingException("Incorrect format of html: invalid timetable")

    weekdays_tag: bs4.Tag = trs[0]
    weekdays: List[str] = [day.text.strip() for day in weekdays_tag.find_all('th')[1:]]
    if len(weekdays) != 6:
        raise TimetableParsingException("Incorrect format of html: invalid number of weekdays")

    cells: List[Cell] = []
    times: List[str] = []

    #  Parsing of times and weekdays
    for tr in trs[1:]:
        tds: bs4.ResultSet = tr.find_all('td')

        if len(tds) != 7:
            raise TimetableParsingException("Incorrect format of html: invalid number of columns in timetable")

        time: str = tds[0].text.strip()
        times.append(time)

        for td in tds[1:]:
            cells.append(parse_cell(td))

    return Timetable(cells=cells, weekdays=weekdays, times=times)


def parse_timetable_from_url(url: str) -> Timetable:
    """
    Parses object of :class:`src.timetable_objects.Timetable` using url of group.

    :param url: url of group, can contain any number of spaces at the beginning and at the end.
    """

    try:
        content: str = download_html(url)
        return parse_timetable_from_html(content)
    except HTMLDownloadingException:
        raise TimetableParsingException(f'Invalid url "{url}"')


def parse_timetable_from_group_id(group_id: str) -> Timetable:
    """
    Parses object of :class:`src.timetable_objects.Timetable` using id of group.

    :param group_id: id of group, can contain any number of spaces at the beginning and at the end.
    """

    if group_id.isspace():
        raise TimetableParsingException('Group id cannot be whitespace-string')

    return parse_timetable_from_url(f'https://table.nsu.ru/group/{group_id.strip()}')
