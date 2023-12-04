from abc import ABC

from services.extraction import Extractor, ExtractionResult, ExtractionCodes
from ..response import Response
from ..response_codes import ResponseCodes


class ExtractionController(ABC):
    __extractor: Extractor

    def __init__(self, extractor: Extractor):
        self.__extractor = extractor

    def get_timetable(self, group_id: str) -> Response:
        extraction_result: ExtractionResult = self.__extractor.extract_timetable(group_id)
        return self.__extraction_result_to_response(extraction_result)

    def get_room(self, room_name: str) -> Response:
        extraction_result: ExtractionResult = self.__extractor.extract_room(room_name)
        return self.__extraction_result_to_response(extraction_result)

    def get_tutor(self, tutor_name: str) -> Response:
        extraction_result: ExtractionResult = self.__extractor.extract_tutor(tutor_name)
        return self.__extraction_result_to_response(extraction_result)

    def get_times(self) -> Response:
        extraction_result: ExtractionResult = self.__extractor.extract_times()
        return self.__extraction_result_to_response(extraction_result)

    @staticmethod
    def __extraction_result_to_response(extraction_result: ExtractionResult) -> Response:
        return Response(
            result=extraction_result.result,
            is_success=extraction_result.is_success,
            message=extraction_result.message,
            code=ExtractionController.__extraction_code_to_response_code(extraction_result.code)
        )

    @staticmethod
    def __extraction_code_to_response_code(code: ExtractionCodes) -> ResponseCodes:
        return ResponseCodes(code.value)
