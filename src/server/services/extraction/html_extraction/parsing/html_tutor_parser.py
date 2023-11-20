from typing import Optional

import bs4

from common import Tutor
from .parsing_exceptions import TutorParsingException, TutorNotFoundException
from .utils import create_html_bs4


class HTMLTutorParser:
    __cannot_parse_tutor_href: str = 'Invalid format of HTML: cannot parse tutor href'

    __tutor_tag_name: str = 'a'
    __tutor_full_name_attr_name: str = 'title'
    __tutor_href_attr_name: str = 'href'

    @staticmethod
    def parse_tutor(html_content: str, tutor_name: str) -> Tutor:
        soup: bs4.BeautifulSoup = create_html_bs4(html_content)
        tutor_tag: Optional[bs4.Tag] = HTMLTutorParser.__find_tutor_tag(soup=soup, tutor_name=tutor_name)

        if tutor_tag is None:
            raise TutorNotFoundException(HTMLTutorParser.__get_tutor_not_found_message(tutor_name))

        return HTMLTutorParser.parse_tutor_from_tag(tutor_tag)

    @staticmethod
    def parse_tutor_from_tag(tutor_tag: bs4.Tag) -> Tutor:
        name: str = tutor_tag.text
        href: Optional[str] = tutor_tag.attrs.get(HTMLTutorParser.__tutor_href_attr_name)

        if href is None:
            raise TutorParsingException(HTMLTutorParser.__cannot_parse_tutor_href)

        return Tutor(name=name, href=href)

    @staticmethod
    def __find_tutor_tag(soup: bs4.BeautifulSoup, tutor_name: str) -> Optional[bs4.Tag]:
        return (
            # Tag found by short name
            HTMLTutorParser.__find_tutor_tag_by_short_name(
                soup=soup,
                short_name=tutor_name,
            )

            or

            # Tag found by full name
            HTMLTutorParser.__find_tutor_tag_by_full_name(
                soup=soup,
                full_name=tutor_name,
            )
        )

    @staticmethod
    def __find_tutor_tag_by_short_name(soup: bs4.BeautifulSoup, short_name: str) -> Optional[bs4.Tag]:
        return soup.find(
            name=HTMLTutorParser.__tutor_tag_name,
            string=short_name,
        )

    @staticmethod
    def __find_tutor_tag_by_full_name(soup: bs4.BeautifulSoup, full_name: str) -> Optional[bs4.Tag]:
        return soup.find(
            name=HTMLTutorParser.__tutor_tag_name,
            attrs={
                HTMLTutorParser.__tutor_full_name_attr_name: full_name,
            }
        )

    @staticmethod
    def __get_tutor_not_found_message(tutor_name: str) -> str:
        return f'Tutor "{tutor_name}" not found'
