from typing import List

import bs4
import requests
from bs4 import ResultSet

from src.timetable_objects import Timetable, Cell
from .timetable_parsing_utils import parse_cell


def parse_timetable_from_html(html_page: str) -> Timetable:
    """
    Parses object of :class:`src.timetable_objects.Timetable` using html-page of timetable.

    :param html_page: string with html-page of timetable.
    """

    soup: bs4.BeautifulSoup = bs4.BeautifulSoup(html_page, 'html.parser')
    timetable_tag: bs4.element.Tag = soup.find('table', {'class': 'time-table'})

    trs: ResultSet = timetable_tag.find_all('tr')

    weekdays_tag: bs4.element.Tag = trs[0]
    weekdays: List[str] = [day.text.strip() for day in weekdays_tag.find_all('th')[1:]]

    cells: List[Cell] = []
    times: List[str] = []

    #  Parsing of times and weekdays
    for tr in trs[1:]:
        tds: ResultSet = tr.find_all('td')

        time: str = tds[0].text.strip()
        times.append(time)

        for q in tds[1:]:
            cells.append(parse_cell(q))

    return Timetable(cells=cells, weekdays=weekdays, times=times)


def parse_timetable_from_url(url: str) -> Timetable:
    """
    Parses object of :class:`src.timetable_objects.Timetable` using url of group.

    :param url: url of group, can contain any number of spaces at the beginning and at the end.
    """

    return parse_timetable_from_html(requests.get(url).text)


def parse_timetable_from_group_id(group_id: str) -> Timetable:
    """
    Parses object of :class:`src.timetable_objects.Timetable` using id of group.

    :param group_id: id of group, can contain any number of spaces at the beginning and at the end.
    """

    return parse_timetable_from_url(f'https://table.nsu.ru/group/{group_id.strip()}')
