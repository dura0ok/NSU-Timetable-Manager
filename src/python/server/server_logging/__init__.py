from logging import Logger
from typing import Optional

import werkzeug
from flask import Request

from common import ServerResponse, Timetable


def __get_remote_addr(_request: Request) -> Optional[str]:
    return _request.remote_addr


def __get_remote_port(_request: Request) -> Optional[int]:
    return _request.environ['REMOTE_PORT']


def __get_request_method(_request: Request) -> str:
    return _request.method


def __get_server_protocol(_request: Request) -> str:
    return _request.environ['SERVER_PROTOCOL']


def __get_path_info(_request: Request) -> str:
    return _request.path


def __get_short_repr_of_response(response: ServerResponse) -> str:
    tmp = response.to_dict()

    if isinstance(response.result, Timetable):
        tmp['result'] = 'Timetable(...)'

    return str(tmp)


def log_request(logger: Logger, _request: Request) -> None:
    remote_addr = __get_remote_addr(_request)
    remote_port = __get_remote_port(_request)
    request_method = __get_request_method(_request)
    server_protocol = __get_server_protocol(_request)
    path_info = __get_path_info(_request)
    logger.info(f'{remote_addr}:{remote_port}    Request:  {request_method} {path_info} {server_protocol}')


def log_response(logger: Logger, response: ServerResponse, _request: Request) -> None:
    remote_addr = __get_remote_addr(_request)
    remote_port = __get_remote_port(_request)
    logger.info(f'{remote_addr}:{remote_port}    Response: {__get_short_repr_of_response(response)}')


def log_http_error(logger: Logger, e: werkzeug.exceptions.HTTPException, _request: Request) -> None:
    remote_addr = __get_remote_addr(_request)
    remote_port = __get_remote_port(_request)
    logger.info(f'{remote_addr}:{remote_port}    Response: {e}')


__all__ = ['log_request', 'log_response', 'log_http_error']
