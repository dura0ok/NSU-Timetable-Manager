from parsing_codes import ParsingCodes
from parsing_exceptions import TutorParsingException
from parsing_result import ParsingResult, create_error_parsing_result
from timetable_objects import Tutor


class HTMLTutorParser:
    @staticmethod
    def parse_tutor(html_content: str, tutor_name: str) -> ParsingResult:
        if html_content.find(tutor_name) == -1:
            return create_error_parsing_result(f'Tutor with name {tutor_name} not found', ParsingCodes.UNKNOWN_TUTOR)

        if tutor_name.find('.') != -1:
            return HTMLTutorParser.__parse_tutor_by_short_name(html_content=html_content, short_name=tutor_name)
        else:
            return HTMLTutorParser.__parse_by_from_full_name(html_content=html_content, full_name=tutor_name)

    @staticmethod
    def __parse_tutor_by_short_name(html_content: str, short_name: str) -> ParsingResult:
        href: str = HTMLTutorParser.__parse_tutor_href_by_short_name(html_content=html_content, short_name=short_name)
        tutor: Tutor = Tutor(name=short_name, href=href)

        return ParsingResult(result=tutor)

    @staticmethod
    def __parse_by_from_full_name(html_content: str, full_name: str) -> ParsingResult:
        href: str = HTMLTutorParser.__parse_tutor_href_by_full_name(html_content=html_content, full_name=full_name)
        name: str = HTMLTutorParser.__parse_tutor_name_by_full_name(html_page=html_content, full_name=full_name)
        tutor: Tutor = Tutor(name=name, href=href)

        return ParsingResult(result=tutor)

    @staticmethod
    def __parse_tutor_href_by_short_name(html_content: str, short_name: str) -> str:
        reversed_html_content: str = html_content[::-1]
        reversed_short_name: str = short_name[::-1]
        reversed_short_name_index: int = reversed_html_content.find(reversed_short_name)

        return HTMLTutorParser.__parse_attr(
            attr_name='href',
            html_page=html_content,
            reversed_html=reversed_html_content,
            end_index=reversed_short_name_index,
            error_message='Invalid format of HTML: cannot parse href of tutor'
        )

    @staticmethod
    def __parse_tutor_href_by_full_name(html_content: str, full_name: str) -> str:
        reversed_html_content: str = html_content[::-1]
        reversed_full_name: str = full_name[::-1]
        reversed_full_name_index: int = reversed_html_content.find(reversed_full_name)

        return HTMLTutorParser.__parse_attr(
            attr_name='href',
            html_page=html_content,
            reversed_html=reversed_html_content,
            end_index=reversed_full_name_index,
            error_message='Invalid format of HTML: cannot parse href of tutor'
        )

    @staticmethod
    def __parse_tutor_name_by_full_name(html_page: str, full_name: str) -> str:
        error_message: str = 'Invalid format of HTML: cannot parse name of tutor'

        i1: int = html_page.find(full_name)

        i2: int = html_page.find('>', i1)
        if i2 == -1:
            raise TutorParsingException(error_message)

        i3: int = html_page.find('<', i2)
        if i3 == -1:
            raise TutorParsingException(error_message)

        return html_page[i2+1:i3]

    @staticmethod
    def __parse_attr(attr_name: str, html_page: str, reversed_html: str, end_index: int, error_message: str) -> str:
        i1: int = reversed_html.find(attr_name[::-1], end_index)
        if i1 == -1:
            raise TutorParsingException(error_message)
        attr_index: int = len(html_page) - i1 + 1
        i2: int = html_page.find('"', attr_index + 2)
        if i2 == -1:
            raise TutorParsingException(error_message)

        return html_page[attr_index + 1:i2]
