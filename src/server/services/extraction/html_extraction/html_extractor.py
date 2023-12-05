from model.dto import Times, Timetable, Room, Tutor
from .downloading import *
from .parsing import *
from .parsing.exceptions import *
from .parsing.utils import get_messages_chain
from ..extraction_codes import ExtractionCodes
from ..extraction_result import ExtractionResult, create_error_extraction_result
from ..extractor import Extractor


class HTMLExtractor(Extractor):
    __group_url: str = 'https://table.nsu.ru/group'
    __room_url: str = 'https://table.nsu.ru/room'
    __all_tutors_url: str = 'https://table.nsu.ru/teacher'
    __times_url: str = 'https://table.nsu.ru'

    def extract_timetable(self, group_id: str) -> ExtractionResult:
        try:
            html_content: str = HTMLDownloader.download(self.__get_group_url(group_id))
            timetable: Timetable = HTMLTimetableParser.parse_timetable(html_content)
        except HTMLDownloadingException:
            return create_error_extraction_result(
                message=HTMLExtractor.__get_cannot_download_timetable_page_message(group_id),
                code=ExtractionCodes.UNKNOWN_GROUP
            )
        except (TimetableParsingException, TimesParsingException) as e:
            return create_error_extraction_result(
                message=get_messages_chain(e),
                code=ExtractionCodes.INTERNAL_ERROR
            )

        return ExtractionResult(timetable)

    def extract_room(self, room_name: str) -> ExtractionResult:
        try:
            html_content: str = HTMLDownloader.download(self.__get_room_url(room_name))
            room: Room = HTMLRoomParser.parse_room(html_content)
        except HTMLDownloadingException:
            return create_error_extraction_result(
                message=HTMLExtractor.__get_cannot_download_room_page_message(room_name),
                code=ExtractionCodes.UNKNOWN_ROOM
            )
        except RoomParsingException as e:
            return create_error_extraction_result(
                message=get_messages_chain(e),
                code=ExtractionCodes.INTERNAL_ERROR
            )

        return ExtractionResult(room)

    def extract_tutor(self, tutor_name: str) -> ExtractionResult:
        try:
            html_content: str = HTMLDownloader.download(HTMLExtractor.__all_tutors_url)
            tutor: Tutor = HTMLTutorParser.parse_tutor(html_content=html_content, tutor_name=tutor_name)
        except HTMLDownloadingException:
            return create_error_extraction_result(
                message=HTMLExtractor.__get_cannot_download_all_tutors_page_message(),
                code=ExtractionCodes.INTERNAL_ERROR
            )
        except TutorParsingException as e:
            return create_error_extraction_result(
                message=str(e),
                code=ExtractionCodes.INTERNAL_ERROR
            )
        except TutorNotFoundException as e:
            return create_error_extraction_result(
                message=get_messages_chain(e),
                code=ExtractionCodes.UNKNOWN_TUTOR,
            )

        return ExtractionResult(tutor)

    def extract_times(self) -> ExtractionResult:
        url: str = HTMLExtractor.__times_url

        try:
            html_content: str = HTMLDownloader.download(url)
            times: Times = HTMLTimesParser.parse_times(html_content)
        except HTMLDownloadingException:
            return create_error_extraction_result(
                message=HTMLExtractor.__get_cannot_download_times_page_message(),
                code=ExtractionCodes.INTERNAL_ERROR
            )
        except TimesParsingException as e:
            return create_error_extraction_result(
                message=get_messages_chain(e),
                code=ExtractionCodes.INTERNAL_ERROR
            )

        return ExtractionResult(times)

    @staticmethod
    def __get_group_url(group_id: str) -> str:
        # valid group id can contain russian 'м', 'М', 'с', 'С', but url must contain only english characters.
        real_group_id = group_id.lower().replace('м', 'm').replace('с', 's')
        return f'{HTMLExtractor.__group_url}/{real_group_id}'

    @staticmethod
    def __get_room_url(room_name: str) -> str:
        return f'{HTMLExtractor.__room_url}/{room_name}'

    @staticmethod
    def __get_cannot_download_timetable_page_message(group_id: str) -> str:
        return f'Group "{group_id}" not found'

    @staticmethod
    def __get_cannot_download_room_page_message(room_name: str) -> str:
        return f'Room "{room_name}" not found'

    @staticmethod
    def __get_cannot_download_all_tutors_page_message() -> str:
        return 'Cannot download page with all tutors'

    @staticmethod
    def __get_cannot_download_times_page_message() -> str:
        return 'Cannot download page with times'
