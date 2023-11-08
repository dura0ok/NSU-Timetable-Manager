from typing import Optional

import bs4

from common import ServerResponse
from common import Tutor, ServerCodes
from common import create_error_server_response
from .parsing_exceptions import TutorParsingException


class HTMLTutorParser:
    @staticmethod
    def parse_tutor(html_content: str, tutor_name: str) -> ServerResponse:
        soup: bs4.BeautifulSoup = bs4.BeautifulSoup(markup=html_content, features='html.parser')
        tutor_tag: Optional[bs4.Tag] = HTMLTutorParser.__extract_tutor_tag(soup=soup, tutor_name=tutor_name)

        if tutor_tag is None:
            return create_error_server_response(
                message=f'Tutor "{tutor_name}" not found',
                code=ServerCodes.UNKNOWN_TUTOR
            )

        try:
            tutor: Tutor = HTMLTutorParser.__parse_tutor_from_tag(tutor_tag=tutor_tag)
        except TutorParsingException as e:
            return create_error_server_response(message=str(e), code=ServerCodes.INTERNAL_ERROR)

        return ServerResponse(tutor)

    @staticmethod
    def __extract_tutor_tag(soup: bs4.BeautifulSoup, tutor_name: str) -> Optional[bs4.Tag]:
        teacher_tag_name: str = 'a'
        return (soup.find(name=teacher_tag_name, attrs={'title': tutor_name}) or
                soup.find(name=teacher_tag_name, string=tutor_name))

    @staticmethod
    def __parse_tutor_from_tag(tutor_tag: bs4.Tag) -> Tutor:
        attrs = tutor_tag.attrs

        name = tutor_tag.text
        if name is None:
            raise TutorParsingException('Invalid format of HTML: cannot parse tutor name')

        href = attrs.get('href')
        if href is None:
            raise TutorParsingException('Invalid format of HTML: cannot parse tutor href')

        return Tutor(name=name, href=href)
