from abc import ABC

from controller import Response
from services.extraction import Extractor


class ExtractionController(ABC):
    __extractor: Extractor

    def get_timetable(self, group_id: str) -> Response:
        pass

    def get_room(self, room_name: str) -> Response:
        pass

    def get_tutor(self, tutor_name: str) -> Response:
        pass

    def get_times(self) -> Response:
        pass
