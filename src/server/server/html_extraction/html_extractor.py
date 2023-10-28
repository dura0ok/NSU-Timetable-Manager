from common.server_codes import ServerCodes
from common.server_response import ServerResponse, create_error_parsing_result
from server.extractor import Extractor
from .downloading import *
from .parsing import *


class HTMLExtractor(Extractor):
    __downloader: HTMLDownloader = HTMLDownloader()

    __timetable_parser: HTMLTimetableParser = HTMLTimetableParser()
    __room_parser: HTMLRoomParser = HTMLRoomParser()
    __tutor_parser: HTMLTutorParser = HTMLTutorParser()
    __times_parser: HTMLTimesParser = HTMLTimesParser()

    def extract_timetable(self, group_id: str) -> ServerResponse:
        striped_group_id: str = group_id.strip()

        try:
            html_content: str = self.__downloader.download(url=self.__get_group_url(striped_group_id))
        except HTMLDownloadingException:
            return create_error_parsing_result(
                message=f'Group {striped_group_id} not found',
                code=ServerCodes.UNKNOWN_GROUP
            )

        return self.__timetable_parser.parse_timetable(html_content=html_content)

    def extract_room(self, room_name: str) -> ServerResponse:
        striped_room_name: str = room_name.strip()

        try:
            html_content: str = self.__downloader.download(url=self.__get_room_url(striped_room_name))
        except HTMLDownloadingException:
            return create_error_parsing_result(
                message=f'Room {striped_room_name} not found',
                code=ServerCodes.UNKNOWN_ROOM
            )

        return self.__room_parser.parse_room(html_content=html_content)

    def extract_tutor(self, tutor_name: str) -> ServerResponse:
        striped_tutor_name: str = tutor_name.strip()
        all_tutors_page_url: str = self.__get_all_tutors_page_url()

        try:
            html_content: str = self.__downloader.download(url=all_tutors_page_url)
        except HTMLDownloadingException:
            return create_error_parsing_result(
                message=f'Cannot parse tutor from {all_tutors_page_url}',
                code=ServerCodes.INTERNAL_ERROR
            )

        return self.__tutor_parser.parse_tutor(html_content=html_content, tutor_name=striped_tutor_name)

    def extract_times(self) -> ServerResponse:
        times_url: str = 'https://table.nsu.ru/'

        try:
            html_content: str = self.__downloader.download(url=times_url)
        except HTMLDownloadingException:
            return create_error_parsing_result(
                message=f'Cannot parse times from {times_url}',
                code=ServerCodes.INTERNAL_ERROR
            )

        return self.__times_parser.parse_times(html_content=html_content)

    @staticmethod
    def __get_group_url(group_id: str) -> str:
        real_group_id = group_id.lower().replace('м', 'm').replace('с', 's')
        return f'https://table.nsu.ru/group/{real_group_id}'

    @staticmethod
    def __get_room_url(room_name: str) -> str:
        url_name: str = ' '.join(room_name.split()).replace(' ', '+')
        return f'https://table.nsu.ru/room/{url_name}'

    @staticmethod
    def __get_all_tutors_page_url() -> str:
        return 'https://table.nsu.ru/teacher'
