from typing import List

import bs4

from .parsing_codes import ParsingCodes
from .parsing_result import ParsingResult, create_error_parsing_result
from .utils import download_html
from src.timetable_objects import Times


def parse_times() -> ParsingResult:
    """
    Parses times of :class:`src.timetable_objects.Timetable` (timestamps when lessons begin) from main page of
    NSU-timetable.
    """

    error_message: str = 'Invalid format of HTML: cannot parse times'

    html_page: str = download_html('https://table.nsu.ru/')
    soup: bs4.BeautifulSoup = bs4.BeautifulSoup(html_page, 'html.parser')

    times_tag: bs4.Tag = soup.find('div', {'class': 'modal-body'})
    if times_tag is None:
        return create_error_parsing_result(error_message, ParsingCodes.INVALID_HTML)

    try:
        times_list: List[str] = [tr.find_all('td')[1].text.split('-')[0] for tr in times_tag.find_all('tr')]
    except IndexError:
        return create_error_parsing_result(error_message, ParsingCodes.INVALID_HTML)

    return ParsingResult(Times(times_list))
