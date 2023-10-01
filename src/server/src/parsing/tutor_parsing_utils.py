import bs4

from .parsing_exceptions import TutorParsingException
from .utils import download_html


def extract_tutor_href(url: str) -> str:
    i1: int = url.find('/teacher')
    if i1 == -1:
        raise TutorParsingException(f'Invalid url of "{url}"')

    i2: int = url.find('#')

    return url[i1:] if i2 == -1 else url[i1:i2]


def parse_attr_from_all_tutors_page(attr_name: str,
                                    html_page: str,
                                    reversed_html_page: str,
                                    end_index: int,
                                    error_message: str) -> str:

    i1: int = reversed_html_page.find(attr_name[::-1], end_index)
    if i1 == -1:
        raise TutorParsingException(error_message)
    attr_index: int = len(html_page) - i1 + 1
    i2: int = html_page.find('"', attr_index + 2)
    if i2 == -1:
        raise TutorParsingException(error_message)

    return html_page[attr_index + 1:i2]


def parse_tutor_name_from_single_tutor_page(html_page: str) -> str:
    error_message: str = 'Invalid format of html: cannot parse tutor name'

    soup: bs4.BeautifulSoup = bs4.BeautifulSoup(html_page, 'html.parser')

    tag1: bs4.Tag = soup.find('ul', {'class': 'breadcrumb'})
    if tag1 is None:
        raise TutorParsingException(error_message)

    tag2: bs4.Tag = tag1.find('li', {'class': 'active'})
    if tag2 is None:
        raise TutorParsingException(error_message)

    return tag2.text.strip()


def parse_tutor_href_by_short_name(html_page: str, short_name: str) -> str:
    reversed_html_page: str = html_page[::-1]
    reversed_short_name: str = short_name[::-1]
    reversed_short_name_index: int = reversed_html_page.find(reversed_short_name)

    return parse_attr_from_all_tutors_page(
        attr_name='href',
        html_page=html_page,
        reversed_html_page=reversed_html_page,
        end_index=reversed_short_name_index,
        error_message='Invalid html: cannot parse href of tutor'
    )


def parse_tutor_name_by_short_name(html_page: str, short_name: str) -> str:
    reversed_html_page: str = html_page[::-1]
    reversed_short_name: str = short_name[::-1]
    reversed_short_name_index: int = reversed_html_page.find(reversed_short_name)

    return parse_attr_from_all_tutors_page(
        attr_name='title',
        html_page=html_page,
        reversed_html_page=reversed_html_page,
        end_index=reversed_short_name_index,
        error_message='Invalid html: cannot parse name of tutor'
    )


def parse_tutor_href_by_full_name(html_page: str, full_name: str) -> str:
    reversed_html_page: str = html_page[::-1]
    reversed_full_name: str = full_name[::-1]
    reversed_full_name_index: int = reversed_html_page.find(reversed_full_name)

    return parse_attr_from_all_tutors_page(
        attr_name='href',
        html_page=html_page,
        reversed_html_page=reversed_html_page,
        end_index=reversed_full_name_index,
        error_message='Invalid html: cannot parse href of tutor'
    )


def parse_tutor_name_by_full_name(html_page: str, full_name: str) -> str:
    error_message: str = 'Invalid html: cannot parse name of tutor'

    i1: int = html_page.find(full_name)

    i2: int = html_page.find('>', i1)
    if i2 == -1:
        raise TutorParsingException(error_message)

    i3: int = html_page.find('<', i2)
    if i3 == -1:
        raise TutorParsingException(error_message)

    return html_page[i2+1:i3]


def get_formatted_tutor_name(tutor_name: str) -> str:
    return ' '.join(tutor_name.strip().split())


def download_tutors_page() -> str:
    return download_html('https://table.nsu.ru/teacher')
