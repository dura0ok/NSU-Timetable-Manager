from typing import List

import bs4
import requests
from bs4 import ResultSet

from src.timetable import Timetable, Cell
from .utils import parse_cell


def parse_timetable_from_html(html: str) -> Timetable:
    soup: bs4.BeautifulSoup = bs4.BeautifulSoup(html, 'html.timetable_parsing')
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


def parse_from_url(url: str) -> Timetable:
    return parse_timetable_from_html(requests.get(url).text)


def parse_from_group_id(group_id: int) -> Timetable:
    return parse_from_url(f'https://table.nsu.ru/group/{group_id}')
