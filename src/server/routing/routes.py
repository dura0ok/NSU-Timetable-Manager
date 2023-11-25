from fastapi import APIRouter, Response

from common.dto import ServerResponse
from services.extraction import Extractor


class Routes:
    __extractor: Extractor
    __router: APIRouter

    def __init__(self, extractor: Extractor) -> None:
        self.__extractor = extractor
        self.__router = APIRouter()
        self.__add_routes()

    @property
    def router(self) -> APIRouter:
        return self.__router

    def __get_timetable(self, group_id: str):
        return Routes.__create_json_response(
            self.__extractor.extract_timetable(Routes.__split_url_word(group_id))
        )

    def __get_room(self, room_name: str):
        return Routes.__create_json_response(
            self.__extractor.extract_room(Routes.__split_url_word(room_name))
        )

    def __get_tutor(self, tutor_name: str):
        return Routes.__create_json_response(
            self.__extractor.extract_tutor(Routes.__split_url_word(tutor_name))
        )

    def __get_times(self):
        return Routes.__create_json_response(
            self.__extractor.extract_times()
        )

    def __add_routes(self) -> None:
        self.__router.add_api_route(path='/timetable/{group_id}', endpoint=self.__get_timetable, methods=['GET'])
        self.__router.add_api_route(path='/room/{room_name}', endpoint=self.__get_room, methods=['GET'])
        self.__router.add_api_route(path='/tutor/{tutor_name}', endpoint=self.__get_tutor, methods=['GET'])
        self.__router.add_api_route(path='/times', endpoint=self.__get_times, methods=['GET'])

    @staticmethod
    def __create_json_response(extraction_result: ServerResponse) -> Response:
        return Response(content=extraction_result.to_json(), media_type='application/json')

    @staticmethod
    def __split_url_word(url_word: str) -> str:
        return ' '.join(url_word.split('+'))
